from abc import ABC, abstractmethod
from typing import Any, Optional

#TODO: SUBJECT TO CHANGE
class BaseRepository(ABC):
    """Abstract base class that enforces a common interface for all repositories."""

    def __init__(self, db_session: Any):
        """Initializes the repository with a database session/connection."""
        self.db_session = db_session

    @abstractmethod
    def get(self, id: Any) -> Optional[Any]:
        """Retrieves an entity by its primary key."""
        pass

    @abstractmethod
    def save(self, data: Any) -> Any:
        """Saves a new entity."""
        pass

    @abstractmethod
    def delete(self, id: Any) -> None:
        """Deletes an entity by its primary key."""
        pass

    @abstractmethod
    def update(self, data: Any) -> Any:
        """Updates an existing entity."""
        pass
    
    