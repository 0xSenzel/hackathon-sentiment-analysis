from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from ..models.models import Base

class PostgresConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresConnection, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Load environment variables
        load_dotenv()
        
        self.config = {
            'dbname': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT', '6543')
        }
        
        # Create engine and session
        url = "postgresql://{0[user]}:{0[password]}@{0[host]}:{0[port]}/{0[dbname]}".format(self.config)
        self.engine = create_engine(url)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self._initialized = True

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def __enter__(self):
        self.session = self.SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close() 