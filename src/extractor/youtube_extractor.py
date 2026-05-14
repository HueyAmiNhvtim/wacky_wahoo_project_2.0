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
            thread_request = self.youtube_client.commentThreads().list(
                part="snippet, replies", # Specify the specific keys that are gonna appear in the response's commentThread resource
                maxResults=100,
                moderationStatus="published",
                textFormat="html",
                videoId=video_id
            )

            while True:
                thread_response = thread_request.execute()
                for comment_thread in thread_response.get("items", []):
                    result += self.__extract_comment_thread(comment_thread)
                    
                next_page_token = thread_response.get("nextPageToken")
                if not next_page_token:
                    break
                
                thread_request = self.youtube_client.commentThreads().list(
                    part="snippet,replies",
                    maxResults=100,
                    moderationStatus="published",
                    textFormat="html",
                    videoId=video_id, 
                    pageToken=next_page_token,
                )
        except HttpError as err:
            print(err) # TODO: May do more in the future
        return result

    def __extract_comment_thread(self, commentThread: dict) -> List[str]:
        # Part of the above comment because it's too long.
        result = []
        top_level_comment = commentThread["snippet"]["topLevelComment"]
        # TODO: you know the pagination thing that Google did for their Youtube API..
        #       Maybe in the future you can try doing that to prevent returning
        #       a massive list of comments to whatever backend we're gonna do.
        #       Hint: perhaps you can return the generator instead.
        #             and yield the comments in batches? in the comment processing pipeline?
        #             ehh, we will get there when we get there I guess.
        result.append(top_level_comment["snippet"]["textDisplay"])
        actual_reply_count = commentThread["snippet"]["totalReplyCount"] # only request when totalreplycount > 0 (avoid wasting quota)
        
        if actual_reply_count > 0:
            retrieved_replies = commentThread.get("replies", {}).get("comments", [])
            retrieved_reply_count = len(retrieved_replies)
            
            # Only call the quota when the retrieved replies are not enough!
            if actual_reply_count != retrieved_reply_count:
                # Loop through the replies of the current top level comment
                replies_request = self.youtube_client.comments().list(
                    part="snippet",
                    maxResults=100,
                    parentId=top_level_comment["id"]
                )
                
                while True:
                    # TODO: of course...gonna have to wrap the execute stuff with the try-catch statement 
                    replies_response = replies_request.execute()
                    for reply in replies_response.get("items", []):
                        result.append(reply["snippet"]["textDisplay"])
                        
                    next_page_token = replies_response.get("nextPageToken")
                    if not next_page_token:
                        break
                        
                    replies_request = self.youtube_client.comments().list(
                        part="snippet",
                        maxResults=100,
                        parentId=top_level_comment["id"],
                        pageToken=next_page_token,
                    ) 
            else:
                for reply in retrieved_replies:
                    result.append(reply["snippet"]["textDisplay"]) 
        return result

    def extract_livechat(self, video_id: str) -> List[str]:
        """Extract live chat logs."""
        result = []
        # TODO: The most major thing is that the majority of Youtube videos are not streams.
        # Check to see if a video is an archived stream or not.
        return result
    

    def extract_video_info(self, video_id: str) -> dict:
        """Extract metadata like title, views, and total comment count."""
        result = dict()
        # TODO: In the future...maybe implement a cache to avoid wasting quota on repeatedly used video.
        try:
            video_request = self.youtube_client.videos().list(
                part="snippet,statistics",
                id=video_id
            )
            video_response = video_request.execute()
            title = video_response["snippet"]["title"]
            views = video_response["statistics"]["viewCount"]
            total_comment_count = video_response["statistics"]["commentCount"]
            
            result["title"] = title
            result["views"] = views
            result["total_comment_count"] = total_comment_count
            return result
        except HttpError as err:
            print(err)
        return result