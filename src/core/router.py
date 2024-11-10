from fastapi import APIRouter
from ..api.routes import sentiment, post, data_sync, comment

router = APIRouter()

def register_routers(app):
    router.include_router(sentiment.router)
    router.include_router(post.router)
    router.include_router(data_sync.router)
    router.include_router(comment.router)
    app.include_router(router) 