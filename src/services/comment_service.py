from datetime import datetime
from src.models.database import Comment
from sqlalchemy.orm import Session

def create_comment(db: Session, post_id: int, content: str, platform: str, created_at: datetime) -> Comment:
    """
    Create a new comment in the database.
    """
    comment = Comment(
        post_id=post_id,
        content=content,
        platform=platform,
        created_at=created_at,
        scraped_at=datetime.utcnow()
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment 

def get_comments(db: Session, skip: int = 0, limit: int = 10) -> list[Comment]:
    """
    Get all comments from the database with pagination.
    """
    return db.query(Comment)\
        .offset(skip)\
        .limit(limit)\
        .all() 