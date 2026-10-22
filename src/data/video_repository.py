from sqlalchemy.orm import Session

from base_repository import BaseRepository
from typing import Optional, List, Dict
from uuid import UUID as UUIDType

from models import Videos

from sqlalchemy import select, update, delete


class VideoRepository(BaseRepository[Videos]):
    def get_by(self, n: Optional[int]=1, offset: Optional[int]=0, **kwargs) -> List[Optional[Videos]]:
        if n == -1:
            return self.get_by_all(**kwargs)
        
    
    def get_by_all(self, **kwargs) -> List[Optional[Videos]]:
        pass
    
    def insert(self, entity: Videos) -> Videos:
        pass
    
    def insert_all(self, entities: Videos) -> List[Videos]:
        pass
    
    def update(self, values: Dict, conditions: Dict) -> int:
        pass
    
    def delete(self, conditions: Dict) -> int:
        pass
    
    def ensure_videos_exist(self, platform_video_ids: List[str]) -> Dict[str, UUIDType]:
        pass