from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.database import Post, Comment, SentimentAnalysis
import random

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM

template = """Question: {question}

Answer: give answer only. no explaination."""

prompt = ChatPromptTemplate.from_template(template)

model = OllamaLLM(model="llama2")

chain = prompt | model 

from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Replace these with your credentials
DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
DB_NAME = "postgres"
DB_PORT = "6543"
DB_USER = "postgres.dooyrxrhioqvuqduzwmc"
DB_PASSWORD = "gd3x57KVq0JI5Q"

# Construct the database URL for SQLAlchemy
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create the engine
engine = create_engine(DATABASE_URL)

# Define the base class for declarative models
Base = declarative_base()

# Example of a simple table (replace with your own table definition if needed)
class ExampleTable(Base):
    __tablename__ = 'example_table'
    id = Column(Integer, primary_key=True)
    name = Column(String)

import sqlite3

import requests
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
# Create the table in the database (if not exists)
# Base.metadata.create_all(engine)
with engine.connect() as connection:
    # Example of a raw SQL query
    result = connection.execute(text("SELECT * FROM mock_up LIMIT 5;"))
    reviews = [row[4] for row in result.fetchall()]
    # Fetch the results of the query

# class SentimentAnalyzerService:
#     def __init__(self):
#         self.llm = Ollama(model="llama2")
        
#     def analyze_sentiment(self, text: str) -> dict:
#         prompt = PromptTemplate(
#             input_variables=["text"],
#             template="""Analyze the sentiment of this text and return JSON format with these fields:
#             - sentiment: (positive/negative/neutral)
#             - score: (float between 0 and 1)
#             - confidence: (float between 0 and 1)
#             Text: {text}
#             """
#         )
#         result = self.llm(prompt.format(text=text))
#         return result
        
#     def generate_mock_data(self, db: Session) -> dict:
#         # Create mock post
#         post = Post(
#             content=f"Mock post {random.randint(1,1000)}",
#             platform="facebook",
#             created_at=datetime.now(),
#             scraped_at=datetime.now()
#         )
#         db.add(post)
#         db.commit()
        
#         # Create mock comments
#         for _ in range(random.randint(3,7)):
#             comment = Comment(
#                 post_id=post.id,
#                 content=f"Mock comment {random.randint(1,1000)}",
#                 platform="facebook",
#                 created_at=datetime.now(),
#                 scraped_at=datetime.now()
#             )
#             db.add(comment)
#             db.commit()
            
#             # Analyze sentiment
#             sentiment_result = self.analyze_sentiment(comment.content)
            
#             analysis = SentimentAnalysis(
#                 comments_id=comment.id,
#                 **sentiment_result,
#                 analyzed_at=datetime.now()
#             )
#             db.add(analysis)
#             db.commit()
        
#         return {"message": "Mock data generated"} 