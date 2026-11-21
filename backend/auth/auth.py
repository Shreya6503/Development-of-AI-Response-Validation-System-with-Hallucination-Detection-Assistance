
import hashlib
import hmac
import sqlite3
import bcrypt

from backend.database.connection import get_connection


def hash_password(password):
    """Create a secure bcrypt password hash."""

    password_bytes = password.encode("utf-8")

    if len(password_bytes) > 72:
        raise ValueError(
            "Password must not exceed 72 bytes."
        )

    return bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    ).decode("utf-8")


def verify_password(password, stored_hash):
    """Verify bcrypt hashes and support legacy SHA-256 hashes."""

    password_bytes = password.encode("utf-8")

    if stored_hash.startswith(("$2a$", "$2b$", "$2y$")):
        if len(password_bytes) > 72:
            return False, False

        try:
            valid = bcrypt.checkpw(
                password_bytes,
                stored_hash.encode("utf-8")
            )
            return valid, False
        except ValueError:
            return False, False

    # Verify an existing SHA-256 password hash.
    legacy_hash = hashlib.sha256(
        password_bytes
    ).hexdigest()

    valid = hmac.compare_digest(
        legacy_hash,
        stored_hash
    )

    return valid, valid


def register_user(username, email, password):
    """Register a new user."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Check email without case sensitivity.
        cursor.execute(
            """
            SELECT id
            FROM users
            WHERE LOWER(email) = LOWER(?)
            """,
            (email.strip(),)
        )

        if cursor.fetchone():
            return False, "Email address is already registered."

        password_hash = hash_password(password)

        cursor.execute(
            """
            INSERT INTO users (
                username,
                email,
                password_hash
            )
            VALUES (?, ?, ?)
            """,
            (
                username.strip(),
                email.strip(),
                password_hash
            )
        )

        connection.commit()

        return True, "Registration successful!"

    except sqlite3.IntegrityError:
        return False, "Username or email already exists."

    except ValueError as error:
        return False, str(error)

    finally:
        connection.close()


def login_user(email, password):
    """Authenticate a user using their email address."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id, username, email, password_hash
            FROM users
            WHERE LOWER(email) = LOWER(?)
            """,
            (email.strip(),)
        )

        user = cursor.fetchone()

        if not user:
            return False, "Invalid email or password."

        valid, needs_upgrade = verify_password(
            password,
            user["password_hash"]
        )

        if not valid:
            return False, "Invalid email or password."

        # Upgrade legacy SHA-256 hashes after successful login.
        if needs_upgrade:
            new_hash = hash_password(password)

            cursor.execute(
                """
                UPDATE users
                SET password_hash = ?
                WHERE id = ?
                """,
                (new_hash, user["id"])
            )

            connection.commit()

        return True, {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }

    finally:
        connection.close()
