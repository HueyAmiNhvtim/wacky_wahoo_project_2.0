# Probably store the credential stuff into a .env file.
# Also probably a main class to log into OAuth stuff.
from base import BaseExtractor
from typing import List


class YoutubeExtractor(BaseExtractor):
    def __init__(self):
        pass

    def extract_comments(self, video_id: str) -> List[str]:
        """Extract post-stream comments."""
        result = []
        return result


    def extract_livechat(self, video_id: str) -> List[str]:
        """Extract live chat logs."""
        result = []
        return result
    

    def extract_video_info(self, video_id: str) -> dict:
        """Extract metadata like title, views, and total comment count."""
        result = dict()
        return result