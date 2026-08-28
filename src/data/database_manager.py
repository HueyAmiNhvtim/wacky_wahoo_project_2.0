from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os
from dotenv import load_dotenv

#TODO: Use SQLALCHEMY-CORE to connect to postgresql. 
# Basically, create table if they do not exist or apply reflection (idk why we would need to do it) onto an existing database if 
# all of them exists.
# Probably use Alembic to handle the database creation and update and table reflection too.......
# Think of it as a version control for your database (or Django's inhouse db migration stuff.)

class DatabaseManager:
    """Handles database connection and schema initialization."""

    def __init__(self, db_path: str, echo: bool=True):
        """
        Initializes the DatabaseManager.
        :param db_path: The file path to the SQLite database.
        """
        self.db_path = db_path
        self.engine = create_engine(
            url=db_path,
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
        """Creates database tables if they do not exist."""
    
        # cursor = connection.cursor()

        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS videos (
        #     id TEXT PRIMARY KEY,
        #     title TEXT NOT NULL,
        #     views INTEGER
        # );
        # """)
        # connection.commit()
        print("Database schema initialized.")
