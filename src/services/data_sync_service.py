from datetime import datetime
import json
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from .post_service import PostService
from .comment_service import create_comment
from ..api.dtos.post import PostCreate

class DataSyncService:
    def __init__(self):
        self._last_synced_id = 0
        self._batch_sizes = {
            1: 10,  # First batch: posts 1-10
            2: 13,  # Second batch: posts 11-13
            3: 15   # Third batch: posts 14-15
        }
        self._current_batch = 1
    
    def _load_json_data(self) -> Dict:
        with open('dashboard/posts_comments.json', 'r') as file:
            return json.load(file)
    
    def _get_batch_posts(self, data: Dict) -> List[Dict]:
        start_id = self._last_synced_id + 1
        end_id = self._batch_sizes[self._current_batch]
        
        return [post for post in data['posts'] 
                if start_id <= int(post['post_id']) <= end_id]
    
    def sync_data(self, db: Session) -> Dict[str, int]:
        if self._current_batch > 3:
            return {"message": "All data has been synced", "synced_count": 0}
        
        data = self._load_json_data()
        batch_posts = self._get_batch_posts(data)
        
        synced_count = 0
        for post_data in batch_posts:
            # Create post
            post_create = PostCreate(
                content=post_data['content'],
                platform=post_data['platform'],
                created_at=post_data['created_at'],
                scraped_at=datetime.utcnow()
            )
            post = PostService.create_post(db, post_create)
            
            # Create comments
            for comment_data in post_data['comments']:
                create_comment(
                    db=db,
                    post_id=post.id,
                    content=comment_data['content'],
                    created_at=comment_data['created_at'],
                    platform=post_data['platform']
                )
            synced_count += 1
        
        self._last_synced_id = self._batch_sizes[self._current_batch]
        self._current_batch += 1
        
        return {
            "message": f"Synced batch {self._current_batch-1}",
            "synced_count": synced_count
        } 