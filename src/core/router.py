from fastapi import FastAPI
from ..api.routes import sentiment, post

def register_routers(app: FastAPI):
    app.include_router(sentiment.router)
    app.include_router(post.router) 