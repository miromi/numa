import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.core.database import Base
from app.core.dependencies import get_db

# Create a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in test database
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the get_db dependency
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestUsersAPI(unittest.TestCase):
    def setUp(self):
        # Create a fresh database for each test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_create_user(self):
        response = client.post(
            "/api/v1/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test User")
        self.assertEqual(data["email"], "test@example.com")

    def test_create_duplicate_user(self):
        # First create a user
        client.post(
            "/api/v1/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        
        # Try to create another user with the same email
        response = client.post(
            "/api/v1/users/",
            json={"name": "Another User", "email": "test@example.com"}
        )
        self.assertEqual(response.status_code, 400)

    def test_get_users(self):
        # First create a user
        client.post(
            "/api/v1/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        
        # Then get all users
        response = client.get("/api/v1/users/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test User")

    def test_get_user(self):
        # First create a user
        create_response = client.post(
            "/api/v1/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        user_id = create_response.json()["id"]
        
        # Then get the user
        response = client.get(f"/api/v1/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test User")

    def test_get_nonexistent_user(self):
        response = client.get("/api/v1/users/999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()