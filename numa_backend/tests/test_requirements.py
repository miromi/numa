import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

class TestRequirementsAPI(unittest.TestCase):
    def setUp(self):
        # Create a fresh database for each test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

    def test_create_requirement(self):
        response = client.post(
            "/api/v1/requirements/",
            json={"title": "Test Requirement", "description": "This is a test requirement", "user_id": 1}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Requirement")
        self.assertEqual(data["description"], "This is a test requirement")
        self.assertEqual(data["user_id"], 1)

    def test_get_requirements(self):
        # First create a requirement
        client.post(
            "/api/v1/requirements/",
            json={"title": "Test Requirement", "description": "This is a test requirement", "user_id": 1}
        )
        
        # Then get all requirements
        response = client.get("/api/v1/requirements/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test Requirement")

if __name__ == "__main__":
    unittest.main()