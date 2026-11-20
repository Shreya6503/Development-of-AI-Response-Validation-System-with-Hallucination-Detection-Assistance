
import hashlib
import sqlite3

from backend.database.connection import get_connection


def hash_password(password):
    """Hash a password before storing it."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, email, password):
    """Register a new user."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
            """,
            (username, email, password_hash)
        )

        connection.commit()
        return True, "Registration successful!"

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    finally:
        connection.close()


def login_user(username, password):
    """Verify user login details."""

    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE username = ? AND password_hash = ?
        """,
        (username, password_hash)
    )

    user = cursor.fetchone()
    connection.close()

    if user:
        return True, dict(user)

    return False, "Invalid username or password."

