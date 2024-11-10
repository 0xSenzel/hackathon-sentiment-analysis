from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ...database.postgres import PostgresConnection
from ...services.comment_service import get_comments
from ..dtos.comment import CommentResponse
from ...models.database import Comment

router = APIRouter(
    prefix="/comments",
    tags=["comments"]
)

postgres = PostgresConnection()

@router.get("/unanalyzed", response_model=List[CommentResponse])
def get_unanalyzed_comments(
    db: Session = Depends(postgres.get_db)
):
    """
    Get all unanalyzed comments, sorted by ID ascending.
    """
    return db.query(Comment)\
        .filter(Comment.is_analyzed == False)\
        .order_by(Comment.id.asc())\
        .all()