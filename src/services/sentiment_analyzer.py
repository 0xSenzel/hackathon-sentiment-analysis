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
        
    def analyze_sentiment(self, review: str) -> dict:
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
    
    def analyze_and_store(self, db: Session, comment_id: int) -> SentimentAnalysis:
        # Get comment
        comment = db.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            raise ValueError(f"Comment with id {comment_id} not found")
            
        # Analyze sentiment
        analysis_result = self.analyze_sentiment(comment.content)
        
        # Create sentiment analysis record
        sentiment_analysis = SentimentService.create_sentiment_analysis(
            db=db,
            comments_id=comment_id,
            sentiment_group=analysis_result["category"],
            sentiment=analysis_result["sentiment"],
            score=analysis_result["score"],
            confidence=analysis_result["confidence"],
            priority="high" if analysis_result["score"] < 5 else "low",
            department=analysis_result["category"]
        )
        
        # Update comment as analyzed
        comment.isAnalyzed = True
        db.commit()
        
        return sentiment_analysis