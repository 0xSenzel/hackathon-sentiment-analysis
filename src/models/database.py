from sqlalchemy import Column, BigInteger, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    platform = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=False)

class Comment(Base):
    __tablename__ = 'comments'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    post_id = Column(BigInteger, ForeignKey('posts.id'))
    content = Column(Text, nullable=False)
    platform = Column(Text)
    created_at = Column(DateTime(timezone=True), nullable=False)
    scraped_at = Column(DateTime(timezone=True), nullable=False)
    is_analyzed = Column(Boolean, default=False)

class SentimentAnalysis(Base):
    __tablename__ = 'sentiment_analysis'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    comments_id = Column(BigInteger, ForeignKey('comments.id'))
    sentiment_group = Column(Text)
    issue_type = Column(Text)
    sentiment = Column(Text)
    score = Column(Float)
    confidence = Column(Float)
    analyzed_at = Column(DateTime(timezone=True), nullable=False)
    priority = Column(Text)
    department = Column(Text)

class IssueTracking(Base):
    __tablename__ = 'issue_tracking'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_name = Column(Text, nullable=False)
    issue_type = Column(Text, nullable=False)
    sentiment_score = Column(Float)
    volume = Column(Integer)
    priority = Column(Text)
    notification_status = Column(Text)
    department = Column(Text)
    notified_at = Column(DateTime(timezone=True))
    resolved_at = Column(DateTime(timezone=True))
    resolved_by = Column(Text)
    effectiveness_score = Column(Float)

class SentimentSummary(Base):
    __tablename__ = 'sentiment_summary'
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_name = Column(Text, nullable=False)
    issue_type = Column(Text, nullable=False)
    total_sentiment_score = Column(Float)
    average_sentiment_score = Column(Float)
    total_volume = Column(Integer)
    priority = Column(Text)
    threshold_met = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())