from sqlalchemy.orm import Session
from ..database.postgres import PostgresConnection

def get_db():
    postgres = PostgresConnection()
    db = next(postgres.get_db())
    try:
        yield db
    finally:
        db.close() 