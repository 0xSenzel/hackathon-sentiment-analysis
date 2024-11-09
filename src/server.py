from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
import random
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from src.data.database.postgres import PostgresConnection
import time
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://app.dronahq.com",
        "https://your-app.dronahq.io"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama
llm = Ollama(model="llama2")

def analyze_sentiment(text):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="Analyze the sentiment of this text and return only one word (positive/negative/neutral): {text}"
    )
    result = llm(prompt.format(text=text))
    return result.strip().lower()

def generate_mock_data():
    with PostgresConnection() as db:
        # Generate a post
        post_content = f"Mock post {random.randint(1,1000)}"
        post_query = """
        INSERT INTO posts (content, platform, created_at, scraped_at)
        VALUES (%s, %s, %s, %s) RETURNING id
        """
        db.session.execute(post_query, (
            post_content, 
            'facebook', 
            datetime.now(), 
            datetime.now()
        ))
        post_id = db.session.execute("SELECT lastval()").scalar()

        # Generate comments
        for _ in range(random.randint(1,5)):
            comment_content = f"Mock comment {random.randint(1,1000)}"
            comment_query = """
            INSERT INTO comments (post_id, content, platform, created_at, scraped_at)
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            """
            db.session.execute(comment_query, (
                post_id,
                comment_content,
                'facebook',
                datetime.now(),
                datetime.now()
            ))
            comment_id = db.session.execute("SELECT lastval()").scalar()

            # Analyze sentiment
            sentiment = analyze_sentiment(comment_content)
            sentiment_query = """
            INSERT INTO sentiment_analysis 
            (comments_id, sentiment_group, sentiment, score, confidence, analyzed_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            db.session.execute(sentiment_query, (
                comment_id,
                'general',
                sentiment,
                random.random(),
                random.random(),
                datetime.now()
            ))

        db.session.commit()

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/generate-data")
async def generate_data(background_tasks: BackgroundTasks):
    background_tasks.add_task(generate_mock_data)
    return {"message": "Data generation started"}

@app.get("/stats")
async def get_stats():
    with PostgresConnection() as db:
        result = db.session.execute("""
            SELECT 
                sentiment,
                COUNT(*) as count,
                AVG(score) as avg_score
            FROM sentiment_analysis
            GROUP BY sentiment
        """)
        return {"stats": [dict(r) for r in result]}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("server:app", host="0.0.0.0", port=port) 