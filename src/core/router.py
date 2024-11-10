from fastapi import APIRouter
from ..api.routes import sentiment, post, data_sync

router = APIRouter()

def register_routers(app):
    router.include_router(sentiment.router)
    router.include_router(post.router)
    router.include_router(data_sync.router)
    app.include_router(router) 