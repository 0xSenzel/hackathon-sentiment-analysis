from datetime import datetime
from sqlalchemy.orm import Session
from ..models.database import SentimentAnalysis, IssueTracking

class SentimentService:
    @staticmethod
    def create_sentiment_analysis(
        db: Session,
        comments_id: int,
        sentiment_group: str,
        sentiment: str,
        score: float,
        confidence: float,
        priority: str,
        department: str
    ) -> SentimentAnalysis:
        sentiment_analysis = SentimentAnalysis(
            comments_id=comments_id,
            sentiment_group=sentiment_group,
            sentiment=sentiment,
            score=score,
            confidence=confidence,
            analyzed_at=datetime.utcnow(),
            priority=priority,
            department=department,
            notified_at=None,
            resolved_at=None,
            resolved_by=None,
            effectiveness_score=None
        )
        
        try:
            db.add(sentiment_analysis)
            db.commit()
            db.refresh(sentiment_analysis)
            return sentiment_analysis
        except Exception as e:
            db.rollback()
            raise e

    @staticmethod
    def create_issue_tracking(
        db: Session,
        group_name: str,
        issue_type: str,
        sentiment_score: float,
        volume: int,
        priority: str,
        department: str
    ) -> IssueTracking:
        issue = IssueTracking(
            group_name=group_name,
            issue_type=issue_type,
            sentiment_score=sentiment_score,
            volume=volume,
            priority=priority,
            notification_status="pending",
            department=department,
            notified_at=None,
            resolved_at=None,
            resolved_by=None,
            effectiveness_score=None
        )
        
        try:
            db.add(issue)
            db.commit()
            db.refresh(issue)
            return issue
        except Exception as e:
            db.rollback()
            raise e 