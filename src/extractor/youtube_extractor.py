# Probably store the credential stuff into a .env file.
# Also probably a main class to log into OAuth stuff.
from googleapiclient.errors import HttpError
from base import BaseExtractor
from typing import List


class YoutubeExtractor(BaseExtractor):
    def __init__(self, youtube_client):
        self.youtube_client = youtube_client

    def extract_comments(self, video_id: str) -> List[str]:
        """Extract post-stream comments."""
        result = []
        try:
            request = self.youtube_client.commentThreads().list(
                part="snippet,replies",
                maxResults=1,
                moderationStatus="published",
                textFormat="html",
                videoId="fAcT-LezxAY"
            )
            response = request.execute()
            # nextPageToken = response.get("nextPageToken", None)
            # while nextPageToken:
            request = self.youtube_client.commentThreads().list(
                part="snippet,replies",
                maxResults=1,
                moderationStatus="published",
                textFormat="html",
                videoId="fAcT-LezxAY"
            )
            response = request.execute()
            # loop through the commentThread request until no more pageToken too!
            for commentThread in response.get("items", []):
                top_level_comment = commentThread["snippet"]["topLevelComment"]
                # Get the ID of the top_level_comment, then use youtube.comments.list() with its id!
                replies = commentThread["replies"]["comments"]
                print(f"Top Level Comment: {top_level_comment['snippet']['textDisplay']}")
                print(f"Top Level Comment ID: {top_level_comment['id']}")
                
                # Loop through the replies....
                replies_request = self.youtube_client.comments().list(
                    part="snippet",
                    maxResults=100,
                    parentId=top_level_comment["id"]
                )
                replies_response = replies_request.execute()
                num_replies = len(replies_response["items"])
                # Number of comments under the top_level_comment
                while next_page_token := replies_response.get("nextPageToken", None):
                    replies_request = self.youtube_client.comments().list(
                        part="snippet",
                        maxResults=100,
                        parentId=top_level_comment["id"],
                        pageToken=next_page_token
                    ) 
                    # of course...gonna have to wrap the execute stuff with the try-catch statement    
                    replies_response = replies_request.execute()
                    num_replies += len(replies_response["items"])
                
                print(f"Number of comments extracted: {1+num_replies}")
                
                # TODO: make sure to output every single reply here! The one from the replies key only
                # output a limited number of comments by default!
                # print(f"The next page token is {nextPageToken}")
                # nextPageToken = response.get("nextPageToken", None)
        except HttpError as err:
            print(err)
        return result


    def extract_livechat(self, video_id: str) -> List[str]:
        """Extract live chat logs."""
        result = []
        return result
    

    def extract_video_info(self, video_id: str) -> dict:
        """Extract metadata like title, views, and total comment count."""
        result = dict()
        return result