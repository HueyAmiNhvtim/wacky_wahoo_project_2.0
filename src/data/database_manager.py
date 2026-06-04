from typing import Optional

#TODO: Use SQLALCHEMY-CORE to connect to postgresql. 
# Basically, create table if they do not exist or apply reflection (idk why we would need to do it) onto an existing database if 
# all of them exists.
# Probably use Alembic to handle the database creation and update and table reflection too.......
# Think of it as a version control for your database (or Django's inhouse db migration stuff.)

class DatabaseManager:
    """Handles database connection and schema initialization."""

    def __init__(self, db_path: str):
        """
        Initializes the DatabaseManager.
        :param db_path: The file path to the SQLite database.
        """
        self.db_path = db_path

    def connect(self):
        """Establishes a connection to the database."""
        pass
        # if self.conn is None:
        #     try:
        #         # self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        #         # # Use Row factory to access columns by name
        #         # self.conn.row_factory = sqlite3.Row
        #         print(f"Successfully connected to database at {self.db_path}")
        #     except sqlite3.Error as e:
        #         print(f"Error connecting to database: {e}")
        #         raise

    def get_connection(self):
        """Returns the active database connection."""
        if self.conn is None:
            self.connect()
        return self.conn

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed.")

    def initialize_schema(self):
        """Creates database tables if they do not exist."""
        connection = self.get_connection()
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
