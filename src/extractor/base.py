from abc import ABC, abstractmethod
from typing import List

class BaseExtractor(ABC):
    """Abstract base class that enforces a common interface for all platform extractors."""
    
    @abstractmethod
    def extract_video_info(self, video_id: str) -> dict:
        """Extract metadata like title, views, and total comment count."""
        pass

    @abstractmethod
    def extract_comments(self, video_id: str) -> List[str]:
        """Extract post-stream comments."""
        pass

    @abstractmethod
    def extract_livechat(self, video_id: str) -> List[str]:
        """Extract live chat logs."""
        pass
    
    