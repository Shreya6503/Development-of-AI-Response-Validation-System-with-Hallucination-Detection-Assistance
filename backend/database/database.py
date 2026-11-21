
import sqlite3
from pathlib import Path
from contextlib import contextmanager

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database storage directory
DATABASE_DIR = BASE_DIR / "data"
DATABASE_PATH = DATABASE_DIR / "app.db"


def initialize_database():
    """Create the database and required tables."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        connection.commit()


@contextmanager
def get_db_connection():
    """Provide a managed database connection."""

    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
