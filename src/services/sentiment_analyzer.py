from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.database import Post, Comment, SentimentAnalysis
import random

class SentimentAnalyzerService:
    def __init__(self):
        self.llm = Ollama(model="llama2")
        
    def analyze_sentiment(self, text: str) -> dict:
        prompt = PromptTemplate(
            input_variables=["text"],
            template="""Analyze the sentiment of this text and return JSON format with these fields:
            - sentiment: (positive/negative/neutral)
            - score: (float between 0 and 1)
            - confidence: (float between 0 and 1)
            Text: {text}
            """
        )
        result = self.llm(prompt.format(text=text))
        return result
        
    def generate_mock_data(self, db: Session) -> dict:
        # Create mock post
        post = Post(
            content=f"Mock post {random.randint(1,1000)}",
            platform="facebook",
            created_at=datetime.now(),
            scraped_at=datetime.now()
        )
        db.add(post)
        db.commit()
        
        # Create mock comments
        for _ in range(random.randint(3,7)):
            comment = Comment(
                post_id=post.id,
                content=f"Mock comment {random.randint(1,1000)}",
                platform="facebook",
                created_at=datetime.now(),
                scraped_at=datetime.now()
            )
            db.add(comment)
            db.commit()
            
            # Analyze sentiment
            sentiment_result = self.analyze_sentiment(comment.content)
            
            analysis = SentimentAnalysis(
                comments_id=comment.id,
                **sentiment_result,
                analyzed_at=datetime.now()
            )
            db.add(analysis)
            db.commit()
        
        return {"message": "Mock data generated"} 