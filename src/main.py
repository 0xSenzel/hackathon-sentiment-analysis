from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import sentiment

app = FastAPI(
    title="Sentiment Analysis API",
    description="API for analyzing sentiment in social media comments",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sentiment.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True) 