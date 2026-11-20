
import sqlite3
from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Database file location
DATABASE_PATH = BASE_DIR / "database.db"


def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the database file and initialize it."""
    connection = get_connection()
    connection.close()
