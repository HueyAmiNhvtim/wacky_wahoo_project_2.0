from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar, List, Dict
from sqlalchemy.orm import Session

T = TypeVar("T")

# Basically, CRUD-style stuff.
# CREATE, READ, UPDATE, DELETE
class BaseRepository(ABC, Generic[T]):
    """Abstract generic base class that enforces a common CRUD interface for all repositories."""

    def __init__(self, session: Session):
        """
        Initializes the repository with an active database session.
        :param session: An active SQLAlchemy Session.
        """
        self.session = session

    @abstractmethod
    def get_by(self, n: Optional[int]=1, offset: Optional[int]=0, **kwargs) -> List[Optional[T]]:
        """
        Retrieves the n number of records that matches the specified information with <offset> initial rows skips
        Default of n is 1. n=-1 will retrieve everything instead regardless of <offset> value
        """
        if n == -1:
            return self.get_by_all(**kwargs)
    
    @abstractmethod
    def get_by_all(self, **kwargs) -> List[Optional[T]]:
        """
        Retrieves every record that matches the specified information
        """
        pass
    
    # Save is fine, it's just getting the info from the scraper (and future TODO: probably from cache?) and save it into the table
    @abstractmethod
    def save(self, entity: T) -> T:
        """Saves a new entity and flushes/persists it into the corresponding table"""
        pass
    
    @abstractmethod
    def save_all(self, entities: List[T]) -> List[T]:
        """Save multiple entities and flushes/persists them into the corresponding table"""
        pass
    
    # Update one.....WIP
    @abstractmethod
    def update(self, values: Dict, conditions: Dict) -> T:
        """Updates existing entities satisfying conditions with values"""
        pass

    @abstractmethod
    def delete(self, conditions: Dict) -> bool:
        """Deletes an entity that matches the values specified in conditions. Returns True if found and deleted, False otherwise."""
        pass