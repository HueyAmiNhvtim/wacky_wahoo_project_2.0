from sqlalchemy.orm import Session

from base_repository import BaseRepository
from typing import Any, Optional, List, Dict

from models import Users

from sqlalchemy import select, update, insert, delete

# I don't think we need func here for aggregate functions tbh, feels like that would make the repo do too much.
# Should be reserved for when we doing actual analytics stuff.
# Maybe...just maybe we could incorporate them for some of the simpler aggregate usecases, but I still think that would make the 
# repo do too much.

class UserRepository(BaseRepository[Users]):
    def __init__(self, session: Session):
        super().__init__(session)
    
    def get_by(self, n: int=1, offset: int=0, **kwargs) -> List[Optional[Users]]:
        if n == -1:
            return self.get_by_all(**kwargs)
        
        stmt = select(Users).filter_by(**kwargs)
        if offset > 0:
            stmt = stmt.offset(offset=offset)
        if n >= 1:
            stmt = stmt.limit(limit=n)
        # scalars are used instead of execute so that we receive the list of User objects rather than list of tuples of values of rows from users
        # select(Users) basically select every single columns from Users
        return list(self.session.scalars(stmt).all())
    
    def get_by_all(self, **kwargs) -> List[Optional[Users]]:
        stmt = select(Users).filter_by(**kwargs)
        return list(self.session.scalars(stmt).all())
    
    def save(self, user: Users):
        pass
    
    def save_all(self, users: List[Users]) -> List[Users]:
        pass
    
    def update(self, values: Dict, conditions: Dict) -> int:
        pass
    
    def delete(self, conditions: Dict) -> bool:
        pass
    