from pydantic import BaseModel
from datetime import datetime

class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    platform: str
    created_at: datetime
    scraped_at: datetime
    is_analyzed: bool = False
    
    class Config:
        from_attributes = True 