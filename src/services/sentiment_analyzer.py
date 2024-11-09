# from langchain_community.llms import Ollama
# from langchain.prompts import PromptTemplate
# from datetime import datetime
# from sqlalchemy.orm import Session
# # from ..models.database import Post, Comment, SentimentAnalysis
# # import random

# from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama.llms import OllamaLLM

# import sqlite3

# import requests
# from langchain_community.utilities.sql_database import SQLDatabase
# from sqlalchemy import create_engine
# from sqlalchemy.pool import StaticPool
# from sqlalchemy import create_engine
# from sqlalchemy import MetaData
# from sqlalchemy import Table, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base

# template = """Question: {question}

# Answer: give answer only. no explaination."""

# prompt = ChatPromptTemplate.from_template(template)

# model = OllamaLLM(model="llama2")

# chain = prompt | model 


# # Replace these with your credentials
# DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
# DB_NAME = "postgres"
# DB_PORT = "6543"
# DB_USER = "postgres.dooyrxrhioqvuqduzwmc"
# DB_PASSWORD = "gd3x57KVq0JI5Q"

# # Construct the database URL for SQLAlchemy
# DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# # Create the engine
# engine = create_engine(DATABASE_URL)

# # Define the base class for declarative models
# Base = declarative_base()

# # Example of a simple table (replace with your own table definition if needed)
# class ExampleTable(Base):
#     __tablename__ = 'example_table'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# # Create the table in the database (if not exists)
# # Base.metadata.create_all(engine)
# with engine.connect() as connection:
#     # Example of a raw SQL query
#     result = connection.execute(text("SELECT * FROM mock_up LIMIT 5;"))
#     reviews = [row[4] for row in result.fetchall()]
#     # Fetch the results of the query

from langchain_core.prompts import ChatPromptTemplate
# from langchain_ollama.llms import OllamaLLM
from sqlalchemy import create_engine, text
from langchain.llms import Ollama
# or
from langchain_community.llms import Ollama

# Initialize LangChain components
template = """Question: {question}
Answer: give answer only. no explaination."""

prompt = ChatPromptTemplate.from_template(template)
model = Ollama(model="llama2")
chain = prompt | model
DB_HOST = "aws-0-ap-southeast-1.pooler.supabase.com"
DB_NAME = "postgres"
DB_PORT = "6543"
DB_USER = "postgres.dooyrxrhioqvuqduzwmc"
DB_PASSWORD = "gd3x57KVq0JI5Q"
# Database configuration
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def analyze_sentiment(review):
    question = f"""Look into this column: '{review}'?
    give answer in list form without header and nothing else:
    Sentiment (positive/negative/neutral),
    Confidence Score (0-10),
    Sentiment Score (0-10),
    Category (payment/security/onboarding/account management)"""
    
    response = chain.invoke({"question": question})
    return response.strip()

def main():
    print("Starting sentiment analysis...\n")
    
    # Get reviews from database
    with engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM mock_up LIMIT 5;"))
        reviews = [row[4] for row in result.fetchall()]  # Assuming review text is in column 4
    
    # Analyze each review
    for i, review in enumerate(reviews, 1):
        print(f"\nReview #{i}:")
        print("-" * 50)
        print(f"Text: {review}")
        sentiment = analyze_sentiment(review)
        print(f"Analysis: {sentiment}")
        print("-" * 50)

if __name__ == "__main__":
    main()