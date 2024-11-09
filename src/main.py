from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from datetime import datetime
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from models.database import Post, Comment, SentimentAnalysis
from database.connection import get_db
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama
llm = Ollama(model="llama2")

def analyze_sentiment(text):
    prompt = PromptTemplate(
        input_variables=["text"],
        template="""Analyze the sentiment of this text and return JSON format with these fields:
        - sentiment: (positive/negative/neutral)
        - score: (float between 0 and 1)
        - confidence: (float between 0 and 1)
        Text: {text}
        """
    )
    result = llm(prompt.format(text=text))
    return result

@app.post("/generate-mock-data")
async def generate_mock_data(background_tasks: BackgroundTasks):
    db = next(get_db())
    
    # Create mock post
    post = Post(
        content=f"Mock post {random.randint(1,1000)}",
        platform="facebook",
        created_at=datetime.now(),
        scraped_at=datetime.now()
    )
    db.add(post)
    db.commit()
    
    # Create mock comments
    for _ in range(random.randint(3,7)):
        comment = Comment(
            post_id=post.id,
            content=f"Mock comment {random.randint(1,1000)}",
            platform="facebook",
            created_at=datetime.now(),
            scraped_at=datetime.now()
        )
        db.add(comment)
        db.commit()
        
        # Analyze sentiment
        sentiment_result = analyze_sentiment(comment.content)
        
        analysis = SentimentAnalysis(
            comments_id=comment.id,
            **sentiment_result,
            analyzed_at=datetime.now()
        )
        db.add(analysis)
        db.commit()
    
    return {"message": "Mock data generated"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 