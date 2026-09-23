from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker
from models import Base

import os
from dotenv import load_dotenv

#TODO: Use SQLALCHEMY-CORE to connect to postgresql. 
# Basically, create table if they do not exist or apply reflection (idk why we would need to do it) onto an existing database if 
# all of them exists.
# Probably use Alembic to handle the database creation and update and table reflection too.......
# Think of it as a version control for your database (or Django's inhouse db migration stuff.)
# Also, we should probably create a logger to log the stuff instead of using print statement.

class DatabaseManager:
    """Handles database connection and schema initialization."""

    def __init__(self, db_path: str, echo: bool=True):
        """
        Initializes the DatabaseManager.
        :param db_path: The file path to the SQLite database.
        """
        load_dotenv(dotenv_path=".env")
        connection_url = URL.create(
            drivername="postgresql+psycopg",
            username=f"{os.getenv('DB_USERNAME')}",
            password=f"{os.getenv('DB_PW')}",
            host=f"{os.getenv('DB_HOST')}",
            database=f"{os.getenv('DB_NAME')}"
        )
            
        self.engine = create_engine(
            url=connection_url,
            echo=True,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600  # 
        )
        self.session_factory = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session_factory()
    
    def close(self):
        """Closes the database connection."""
        if self.engine:
            self.engine.dispose()
            print("Closing engine...")

    def initialize_schema(self):
        """
        Creates database tables if they do not exist.
        ONLY USABLE FOR unit testing and such. For production (is it even production if this thing is just used for non-commercial purposes?)
        use alembic (and probably poetry too )
        """
        #TODO: I think we should use Alembic for this.
        # Sth like an initial migration if there's nothing there.
        # We will auto assume that if sth is already there, then just use the tables as they are.
        # If there's error, we just log the error and shut the whole thing down. I think.
        Base.metadata.create_all(bind=self.engine)
        print("Database schema initialized.")
