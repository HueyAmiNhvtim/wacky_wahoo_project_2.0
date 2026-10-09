from sqlalchemy.orm import Session

from base_repository import BaseRepository
from typing import Any, Optional, List, Dict

from models import Users

from sqlalchemy import select


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session)
    
    def get_by(self, n: Optional[int]=1, offset: Optional[int]=0, **kwargs) -> List[Optional[]]:
        if n == -1:
            return self.get_by_all(**kwargs)
        
    
    def get_by_all(self, **kwargs) -> List[Optional[]]:
        pass
    
    def save(self, user):
        pass
    
    def save_all(self, users) -> List[]:
        pass
    
    def update(self, values: Dict, conditions: Dict) -> :
        pass
    
    def delete(self, conditions: Dict) -> bool:
        pass
    