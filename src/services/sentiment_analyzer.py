from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from sqlalchemy.orm import Session
from datetime import datetime
from ..models.database import Comment, SentimentAnalysis
from .sentiment_service import SentimentService

class SentimentAnalyzerService:
    def __init__(self):
        # Initialize LangChain components
        template = """Question: {question}
        Answer: give answer only. no explaination."""
        
        self.prompt = ChatPromptTemplate.from_template(template)
        self.model = Ollama(model="llama2")
        self.chain = self.prompt | self.model
        
        # Define thresholds
        self.SENTIMENT_THRESHOLD = -5.0  # Negative threshold for alerts
        self.VOLUME_THRESHOLD = 3  # Minimum number of comments for an issue
        
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
    
    def update_sentiment_summary(self, db: Session, category: str, sentiment_score: float) -> None:
        """Update sentiment summary for the category"""
        SentimentService.upsert_sentiment_summary(
            db=db,
            group_name=category,
            issue_type=category,
            total_sentiment_score=sentiment_score,
            average_sentiment_score=sentiment_score,  # Will be averaged in the service
            total_volume=1,
            priority="high" if sentiment_score < self.SENTIMENT_THRESHOLD else "low",
            threshold_met=sentiment_score < self.SENTIMENT_THRESHOLD
        )

    def check_and_create_issue(self, db: Session, category: str, sentiment_score: float) -> None:
        """Check threshold and create issue if needed"""
        if sentiment_score < self.SENTIMENT_THRESHOLD:
            SentimentService.create_issue_tracking(
                db=db,
                group_name=category,
                issue_type=category,
                sentiment_score=sentiment_score,
                volume=1,
                priority="high",
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
                    priority="high" if analysis["score"] < self.SENTIMENT_THRESHOLD else "low",
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