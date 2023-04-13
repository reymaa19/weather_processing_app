"""This module contains the context manager for the database. """
import sqlite3

class DBCM:
    """
    The DBCM class manages database connections.
    """

    def __init__(self, path: str):
        """Constructor that stores database path name."""
        self.db_name = path
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def __enter__(self):
        """Establishes database connection"""
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Closes the database connection.
        """
        self.conn.commit()
        self.cursor.close()
        self.conn.close()