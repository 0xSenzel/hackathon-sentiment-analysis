from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    platform = Column(String(100))
    created_at = Column(DateTime, nullable=False)
    scraped_at = Column(DateTime, nullable=False)

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    content = Column(Text, nullable=False)
    platform = Column(String(100))
    created_at = Column(DateTime, nullable=False)
    scraped_at = Column(DateTime, nullable=False)

class SentimentAnalysis(Base):
    __tablename__ = 'sentiment_analysis'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    comments_id = Column(Integer, ForeignKey('comments.id'))
    sentiment_group = Column(String(50))
    sentiment = Column(String(20))
    score = Column(Float)
    confidence = Column(Float)
    analyzed_at = Column(DateTime, nullable=False)
    priority = Column(String(20))
    department = Column(String(255))
    notified_at = Column(DateTime)
    resolved_at = Column(DateTime)
    resolved_by = Column(String(255))
    effectiveness_score = Column(Float)

class IssueTracking(Base):
    __tablename__ = 'issue_tracking'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255), nullable=False)
    issue_type = Column(String(50), nullable=False)
    sentiment_score = Column(Float)
    volume = Column(Integer)
    priority = Column(String(20))
    notification_status = Column(String(20))
    department = Column(String(255))
    notified_at = Column(DateTime)
    resolved_at = Column(DateTime)
    resolved_by = Column(String(255))
    effectiveness_score = Column(Float)

class SentimentSummary(Base):
    __tablename__ = 'sentiment_summary'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String(255), nullable=False)
    issue_type = Column(String(50), nullable=False)
    total_sentiment_score = Column(Float)
    average_sentiment_score = Column(Float)
    total_volume = Column(Integer)
    priority = Column(String(20))
    threshold_met = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now()) 