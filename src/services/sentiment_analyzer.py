from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.database import Comment, SentimentAnalysis, SentimentSummary
from .sentiment_service import SentimentService

class SentimentAnalyzerService:
    def __init__(self):
        # Initialize LangChain components
        template = """Question: {question}
                Answer: "Analyze the sentiment of the review. Output your answer as JSON that "
                "matches the given schema: ```json\n{schema}\n```. "
                "Make sure to wrap the answer in ```json and ``` tags"""
        
        self.prompt = ChatPromptTemplate.from_template(template)
        self.model = Ollama(model="llama2")
        self.chain = self.prompt | self.model
        
        # Updated thresholds
        self.SENTIMENT_THRESHOLDS = {
            "high": -0.7,    # Very negative sentiment
            "medium": -0.4,  # Moderately negative
            "low": -0.2      # Slightly negative
        }
        self.VOLUME_THRESHOLDS = {
            "high": 3,       # Immediate attention needed
            "medium": 5,     # Monitor closely
            "low": 10        # General monitoring
        }

    def get_unanalyzed_comments(self, db: Session) -> list[Comment]:
        """Pull all latest unanalyzed comments"""
        return db.query(Comment)\
            .filter(Comment.is_analyzed == False)\
            .order_by(Comment.id.asc())\
            .all()

    def analyze_sentiment(self, review: str) -> dict:
        """Analyze sentiment using langchain components"""
        question = f"""Look into this column: '{review}'?
        give answer in list form without header and nothing else:
        Sentiment (positive/negative/neutral),
        Confidence Score (0-10),
        Sentiment Score (0-10),
        Category (payment/security/onboarding/account management)"""
        
        response = self.chain.invoke({"question": question})
        results = response.strip().split(',')
        
        return {
            "sentiment": results[0].strip(),
            "confidence": float(results[1].strip()),
            "score": float(results[2].strip()),
            "category": results[3].strip()
        }
    
    def determine_priority(self, sentiment_score: float, volume: int) -> tuple[str, bool]:
        """Determine priority and threshold status based on sentiment and volume"""
        if sentiment_score < self.SENTIMENT_THRESHOLDS["high"]:
            return "high", True
        elif sentiment_score < self.SENTIMENT_THRESHOLDS["medium"] and volume >= self.VOLUME_THRESHOLDS["high"]:
            return "medium", True
        elif sentiment_score < self.SENTIMENT_THRESHOLDS["low"] and volume >= self.VOLUME_THRESHOLDS["medium"]:
            return "low", True
        return "normal", False

    def update_sentiment_summary(self, db: Session, category: str, sentiment_score: float) -> None:
        """Update sentiment summary for the category"""
        # Get current volume from existing summary
        existing_summary = db.query(SentimentSummary).filter(
            SentimentSummary.group_name == category
        ).first()
        
        current_volume = 1 if not existing_summary else existing_summary.total_volume + 1
        priority, threshold_met = self.determine_priority(sentiment_score, current_volume)
        
        SentimentService.upsert_sentiment_summary(
            db=db,
            group_name=category,
            issue_type=category,
            sentiment_score=sentiment_score,  # Changed to pass individual score
            volume=1,                         # Changed to pass individual volume
            priority=priority,
            threshold_met=threshold_met
        )

    def check_and_create_issue(self, db: Session, category: str, sentiment_score: float) -> None:
        """Check threshold and create issue if needed"""
        existing_summary = db.query(SentimentSummary).filter(
            SentimentSummary.group_name == category
        ).first()
        
        current_volume = 1 if not existing_summary else existing_summary.total_volume + 1
        priority, threshold_met = self.determine_priority(sentiment_score, current_volume)
        
        if threshold_met:
            SentimentService.create_issue_tracking(
                db=db,
                group_name=category,
                issue_type=category,
                sentiment_score=sentiment_score,
                volume=current_volume,
                priority=priority,
                department=self.get_department_for_category(category)
            )

    def get_department_for_category(self, category: str) -> str:
        """Map category to department"""
        department_mapping = {
            "payment": "Finance",
            "security": "IT Security",
            "onboarding": "Customer Service",
            "account management": "Account Management"
        }
        return department_mapping.get(category, "General Support")

    def process_comments(self, db: Session) -> dict:
        """Main processing function"""
        comments = self.get_unanalyzed_comments(db)
        processed_count = 0
        
        for comment in comments:
            try:
                # Analyze sentiment
                analysis = self.analyze_sentiment(comment.content)
                
                # Store sentiment analysis
                sentiment_analysis = SentimentService.create_sentiment_analysis(
                    db=db,
                    comments_id=comment.id,
                    sentiment_group=analysis["category"],
                    sentiment=analysis["sentiment"],
                    score=analysis["score"],
                    confidence=analysis["confidence"],
                    priority="high" if analysis["score"] < self.SENTIMENT_THRESHOLDS["high"] else "low",
                    department=self.get_department_for_category(analysis["category"])
                )
                
                # Update summary
                self.update_sentiment_summary(db, analysis["category"], analysis["score"])
                
                # Check threshold and create issue if needed
                self.check_and_create_issue(db, analysis["category"], analysis["score"])
                
                # Mark comment as analyzed
                comment.is_analyzed = True
                db.commit()
                
                processed_count += 1
                
            except Exception as e:
                db.rollback()
                print(f"Error processing comment {comment.id}: {str(e)}")
                continue
        
        return {
            "processed_comments": processed_count,
            "status": "completed"
        }