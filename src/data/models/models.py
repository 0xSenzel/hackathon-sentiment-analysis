from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class FacebookComment(Base):
    __tablename__ = 'facebook_comments'

    comment_id = Column(String, primary_key=True)
    user_name = Column(String(255), nullable=False)
    comment_text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    likes = Column(Integer, default=0)
    replies = Column(Integer, default=0)

    def __repr__(self):
        return f"<FacebookComment(comment_id={self.comment_id}, user_name={self.user_name})>" 