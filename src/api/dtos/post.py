from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    content: str
    platform: str
    
class PostResponse(BaseModel):
    id: int
    content: str
    platform: str
    created_at: datetime
    scraped_at: datetime
    
    class Config:
        from_attributes = True 