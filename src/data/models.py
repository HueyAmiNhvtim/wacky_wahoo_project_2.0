from sqlalchemy.orm import DeclarativeBase
from typing import List, Optional

from sqlalchemy import String, Integer, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy import func

# Separate the models layer from the repositories to allow separation of responsibilities
# The models describe what the data looks like, while the repositories describes how to perform operataions to get them.
class Base(DeclarativeBase): # This class already contains the MetaData object, basically maps the SQL table to its string name
    pass

class Videos(Base):
    __tablename__ = "videos"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    platform_video_id: Mapped[str] = mapped_column(String(100), unique=True, index=True) # Youtube's video_id (and probably livestream id) max length is 11 chars, Idk about Twitch's tho, so I'm gonna put 100 just in case.
    name: Mapped[str] = mapped_column(String(100))  # Youtube video title limit is 100 characters. That's good. Free constraint!
    published_at: Mapped[DateTime] = mapped_column(insert_default=func.now()) # So you don't have to include the type name inside mapped_column
    view_count: Mapped[int] = mapped_column(insert_default=0)  # Should we make published_at, view_count, and comment_count capable of being null?
    comment_count: Mapped[int] = mapped_column(insert_default=0)
        
class Comments(Base):
    __tablename__ = "comments"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
class LiveComments(Base):
    __tablename__ = "livecomments"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

class Users(Base): 
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    platform_user_id: Mapped[str] = mapped_column(String(100), unique=True, index=True)


# TODO: Model the relationships too. We will also have to use junction tables to model some of the many-to-many relationships!
# TODO: Still have to define junction tables and relationships. I think the only junction table we need is for videos and users
#       Since youtube (and Twitch) has this thing where multiple users (or streamers) can collaborate on a single video/stream.