from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...database.postgres import PostgresConnection
from ...services.data_sync_service import DataSyncService

router = APIRouter(
    prefix="/data-sync",
    tags=["data-sync"]
)

data_sync_service = DataSyncService()
postgres = PostgresConnection()

@router.post("/")
def sync_data(db: Session = Depends(postgres.get_db)):
    """
    Sync data from JSON file in batches.
    First call: Updates posts 1-10 with comments
    Second call: Updates posts 11-13 with comments
    Third call: Updates posts 14-15 with comments
    """
    return data_sync_service.sync_data(db) 