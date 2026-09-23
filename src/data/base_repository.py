from abc import ABC, abstractmethod
from typing import Any, Generic, List, Optional, TypeVar
from sqlalchemy.orm import Session

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract generic base class that enforces a common CRUD interface for all repositories."""

    def __init__(self, session: Session):
        """
        Initializes the repository with an active database session.
        :param session: An active SQLAlchemy Session.
        """
        self.session = session

    @abstractmethod
    def get(self, id: Any) -> Optional[T]:
        """Retrieves an entity by its primary key."""
        pass

    @abstractmethod
    def save(self, entity: T) -> T:
        """Saves a new entity and flushes/persists it."""
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        """Updates an existing entity."""
        pass

    @abstractmethod
    def delete(self, id: Any) -> bool:
        """Deletes an entity by its primary key. Returns True if found and deleted, False otherwise."""
        pass