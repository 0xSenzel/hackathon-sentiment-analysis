from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ...utils.config import load_config
from ..models.models import Base
import os
from dotenv import load_dotenv

class PostgresConnection:
    def __init__(self, config=None):
        # Load environment variables
        load_dotenv()
        
        self.config = {
            'dbname': os.getenv('DB_NAME', 'postgres'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST'),
            'port': os.getenv('DB_PORT', '6543')
        }
        self.engine = None
        self.Session = None
        self.session = None

    def connect(self):
        """Establish connection to PostgreSQL database using SQLAlchemy"""
        try:
            url = f"postgresql://{self.config['user']}:{self.config['password']}@{self.config['host']}:{self.config['port']}/{self.config['dbname']}"
            self.engine = create_engine(url)
            Base.metadata.create_all(self.engine)
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            print("Successfully connected to PostgreSQL database")
            return True
        except Exception as e:
            print(f"Error connecting to PostgreSQL database: {str(e)}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.session:
            self.session.close()
            print("Database connection closed")

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect() 