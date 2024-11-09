from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...services.post_service import PostService
from ...api.dtos.post import PostCreate, PostResponse
from ...api.dependencies import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return PostService.create_post(db, post) 

@router.get("/", response_model=list[PostResponse])
def get_posts(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return PostService.get_posts(db, skip=skip, limit=limit)