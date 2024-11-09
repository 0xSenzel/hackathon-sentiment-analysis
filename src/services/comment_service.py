from datetime import datetime
from src.models.database import Comment
from sqlalchemy.orm import Session

def create_comment(db: Session, post_id: int, content: str, platform: str) -> Comment:
    """
    Create a new comment in the database.
    """
    comment = Comment(
        post_id=post_id,
        content=content,
        platform=platform,
        created_at=datetime.utcnow(),
        scraped_at=datetime.utcnow()
    )
    
    db.add(comment)
    db.commit()
    db.refresh(comment)
    
    return comment 