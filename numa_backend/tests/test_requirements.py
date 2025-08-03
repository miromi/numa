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

class TestRequirementsAPI(unittest.TestCase):
    def setUp(self):
        # Create a fresh database for each test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        # Create a user for testing
        user_response = client.post(
            "/api/v1/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        self.user_id = user_response.json()["id"]
        
        # Create a requirement first to get a valid requirement_id
        requirement_response = client.post(
            "/api/v1/requirements/",
            json={
                "title": "Test Requirement",
                "description": "This is a test requirement",
                "user_id": self.user_id
            }
        )
        self.requirement_id = requirement_response.json()["id"]
        
        # Create a solution linked to the requirement
        solution_response = client.post(
            "/api/v1/solutions/",
            json={
                "title": "Test Solution",
                "description": "This is a test solution",
                "requirement_id": self.requirement_id
            }
        )
        self.solution_id = solution_response.json()["id"]
        
        # Create a development task linked to the solution
        dev_task_response = client.post(
            "/api/v1/development/",
            json={
                "title": "Test Development Task",
                "description": "This is a test development task",
                "solution_id": self.solution_id,
                "assigned_to": self.user_id
            }
        )
        self.dev_task_id = dev_task_response.json()["id"]
        
        # Create an application linked to the development task
        app_response = client.post(
            "/api/v1/applications/",
            json={
                "name": "Test Application",
                "description": "This is a test application",
                "development_task_id": self.dev_task_id,
                "created_by": self.user_id
            }
        )
        self.app_id = app_response.json()["id"]

    def test_create_requirement(self):
        response = client.post(
            "/api/v1/requirements/",
            json={
                "title": "Test Requirement 2",
                "description": "This is another test requirement",
                "user_id": self.user_id
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Requirement 2")
        self.assertEqual(data["description"], "This is another test requirement")
        self.assertEqual(data["user_id"], self.user_id)

    def test_create_requirement_with_application(self):
        response = client.post(
            "/api/v1/requirements/",
            json={
                "title": "Test Requirement with App",
                "description": "This is a test requirement linked to an app",
                "user_id": self.user_id,
                "application_id": self.app_id
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Requirement with App")
        self.assertEqual(data["description"], "This is a test requirement linked to an app")
        self.assertEqual(data["user_id"], self.user_id)
        self.assertEqual(data["application_id"], self.app_id)

    def test_create_requirement_with_invalid_user(self):
        response = client.post(
            "/api/v1/requirements/",
            json={
                "title": "Test Requirement",
                "description": "This is a test requirement",
                "user_id": 999
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_create_requirement_with_invalid_application(self):
        response = client.post(
            "/api/v1/requirements/",
            json={
                "title": "Test Requirement",
                "description": "This is a test requirement",
                "user_id": self.user_id,
                "application_id": 999
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_get_requirements(self):
        # First create a requirement
        client.post(
            "/api/v1/requirements/",
            json={
                "title": "Test Requirement",
                "description": "This is a test requirement",
                "user_id": self.user_id
            }
        )
        
        # Then get all requirements
        response = client.get("/api/v1/requirements/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreaterEqual(len(data), 1)  # At least one requirement should exist

    def test_get_requirement(self):
        # Use the requirement created in setUp
        response = client.get(f"/api/v1/requirements/{self.requirement_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Requirement")

    def test_get_nonexistent_requirement(self):
        response = client.get("/api/v1/requirements/999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()