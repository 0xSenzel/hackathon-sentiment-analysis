import json
import time
import random
from datetime import datetime
from pathlib import Path
import schedule
from faker import Faker
from ..database.postgres import PostgresConnection
from ..models.models import FacebookComment

class FacebookScraper:
    def __init__(self, config):
        self.config = config
        self.fake = Faker()
        self.mock_data_path = Path("src/data/mock/facebook_comments.json")
        self.mock_data_path.parent.mkdir(parents=True, exist_ok=True)
        
        if not self.mock_data_path.exists():
            self._create_initial_mock_data()

    def _generate_comment(self):
        """Generate a single mock comment"""
        return {
            'comment_id': str(random.randint(10000, 99999)),
            'user_name': self.fake.name(),
            'comment_text': self.fake.text(max_nb_chars=200),
            'timestamp': datetime.now(),
            'likes': random.randint(0, 1000),
            'replies': random.randint(0, 50)
        }

    def _create_initial_mock_data(self):
        """Create initial mock data file"""
        initial_data = [self._generate_comment() for _ in range(50)]
        with open(self.mock_data_path, 'w') as f:
            json.dump([{**d, 'timestamp': d['timestamp'].isoformat()} 
                      for d in initial_data], f, indent=2)

    def _append_new_mock_data(self):
        """Append new mock comments to existing data"""
        try:
            with open(self.mock_data_path, 'r') as f:
                existing_data = json.load(f)
            
            new_comments = [self._generate_comment() 
                          for _ in range(random.randint(5, 10))]
            
            updated_data = existing_data + [{**d, 'timestamp': d['timestamp'].isoformat()} 
                                          for d in new_comments]
            with open(self.mock_data_path, 'w') as f:
                json.dump(updated_data, f, indent=2)
            
            return new_comments
        except Exception as e:
            print(f"Error updating mock data: {str(e)}")
            return []

    def fetch_comments(self):
        """Fetch new comments and save to database using SQLAlchemy"""
        new_comments = self._append_new_mock_data()
        
        if new_comments:
            with PostgresConnection() as db:
                try:
                    # Convert dictionaries to SQLAlchemy models
                    comment_models = [
                        FacebookComment(**comment) 
                        for comment in new_comments
                    ]
                    
                    # Add all new comments
                    db.session.add_all(comment_models)
                    
                    # Commit the transaction
                    db.session.commit()
                    print(f"Saved {len(new_comments)} new comments to database")
                except Exception as e:
                    db.session.rollback()
                    print(f"Error saving to database: {str(e)}")

    def start_scheduled_updates(self):
        """Start scheduled updates every 5 minutes"""
        schedule.every(5).minutes.do(self.fetch_comments)
        
        while True:
            schedule.run_pending()
            time.sleep(1)