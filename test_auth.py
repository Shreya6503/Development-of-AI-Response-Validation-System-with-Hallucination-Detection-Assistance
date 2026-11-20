
from backend.database.connection import initialize_database
from backend.auth.auth import register_user, login_user

# Create database tables
initialize_database()

# Register a test user
success, message = register_user(
    "testuser01",
    "testuser01@example.com",
    "TestPassword123!"
)

print("Registration:", message)

# Test login
success, result = login_user(
    "testuser01",
    "TestPassword123!"
)

print("Login:", "Successful" if success else result)
