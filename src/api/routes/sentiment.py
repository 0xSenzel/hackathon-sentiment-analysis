from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...services.sentiment_analyzer import SentimentAnalyzerService
from ...api.dependencies import get_db

router = APIRouter(
    prefix="/sentiment",
    tags=["sentiment"]
)

sentiment_service = SentimentAnalyzerService()

@router.post("/generate-mock-data")
async def generate_mock_data(db: Session = Depends(get_db)):
    return sentiment_service.generate_mock_data(db) 