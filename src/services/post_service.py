from sqlalchemy.orm import Session
from datetime import datetime
from ..models.database import Post
from ..api.dtos.post import PostCreate, PostResponse

class PostService:
    @staticmethod
    def create_post(db: Session, post: PostCreate) -> PostResponse:
        db_post = Post(
            content=post.content,
            platform=post.platform,
            created_at=datetime.now(),
            scraped_at=datetime.now()
        )
        
        try:
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            return PostResponse.model_validate(db_post)
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_posts(db: Session, skip: int = 0, limit: int = 10):
        return db.query(Post).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_post(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()
    
    @staticmethod
    def delete_post(db: Session, post_id: int):
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            db.delete(post)
            db.commit()
            return True
        return False 