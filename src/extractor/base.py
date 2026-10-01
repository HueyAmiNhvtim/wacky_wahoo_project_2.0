from abc import ABC, abstractmethod
from typing import List

# TODO: Ok, we have to agree upon the data returned by the extractors...so that we could know how to properly insert stuff
# DATA FORMAT RETURNED BY the extractors, CHANGE IF YOU'RE GONNA MODIFY THE EXTRACTORS:

# Tho, in the future....stuff like comments and livechats or users are probably gonna be generator objects instead?
# This is based on the models.py
# {
#   'video': {
#       platform_video_id: 
#       title: 
#       published_at:
#       view_count:
#       comment_count:
#       is_livestream:
#   },
#   'comments': [{
#       platform_comment_id: 
#       published_at:
#       text:
#   }, {more_dictionary}],
#   'livechats': [{
#       platform_comment_id: 
#       published_at:
#       text: 
#   }, {more_dictionary}],
#   'users': {
#       platform_video_id: []
#   }
# }


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
    
    # There is still the users thing, tho I think it is the responsibility of the extractors to output that
    @abstractmethod
    def extract_everything(self, video_id: str) -> dict:
        info = dict()
        info["video"] = self.extract_video_info(video_id=video_id)
        if info["has_livechats"]:
            livechats = self.extract_livechat(video_id=video_id)
            info["livechats"] = livechats
        else:
            info["livechats"] = []
        comments = self.extract_comments(video_id=video_id)
        info["comments"] = comments
        
        # WIP
        info["users"] = []
        return info
        
    
    