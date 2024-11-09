from datetime import datetime
from sqlalchemy.orm import Session
from ..models.database import SentimentAnalysis, IssueTracking, SentimentSummary

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

    @staticmethod
    def get_issues_by_notification_status(
        db: Session, 
        notification_status: str,
        skip: int = 0,
        limit: int = 10
    ) -> list[IssueTracking]:
        return db.query(IssueTracking)\
            .filter(IssueTracking.notification_status == notification_status)\
            .order_by(IssueTracking.notified_at.asc())\
            .offset(skip)\
            .limit(limit)\
            .all() 

    @staticmethod
    def upsert_sentiment_summary(
        db: Session,
        group_name: str,
        issue_type: str,
        total_sentiment_score: float,
        average_sentiment_score: float,
        total_volume: int,
        priority: str,
        threshold_met: bool = False
    ) -> SentimentSummary:
        # Check if record exists
        existing_summary = db.query(SentimentSummary).filter(
            SentimentSummary.group_name == group_name,
            SentimentSummary.issue_type == issue_type
        ).first()
        
        if existing_summary:
            # Update existing record
            existing_summary.total_sentiment_score = total_sentiment_score
            existing_summary.average_sentiment_score = average_sentiment_score
            existing_summary.total_volume = total_volume
            existing_summary.priority = priority
            existing_summary.threshold_met = threshold_met
            existing_summary.updated_at = datetime.utcnow()
            
            try:
                db.commit()
                db.refresh(existing_summary)
                return existing_summary
            except Exception as e:
                db.rollback()
                raise e
        else:
            # Create new record
            new_summary = SentimentSummary(
                group_name=group_name,
                issue_type=issue_type,
                total_sentiment_score=total_sentiment_score,
                average_sentiment_score=average_sentiment_score,
                total_volume=total_volume,
                priority=priority,
                threshold_met=threshold_met,
                created_at=datetime.utcnow()
            )
            
            try:
                db.add(new_summary)
                db.commit()
                db.refresh(new_summary)
                return new_summary
            except Exception as e:
                db.rollback()
                raise e