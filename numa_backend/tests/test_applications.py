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

class TestApplicationsAPI(unittest.TestCase):
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
        
        # Create a requirement for testing
        requirement_response = client.post(
            "/api/v1/requirements/",
            json={"title": "Test Requirement", "description": "This is a test requirement", "user_id": self.user_id}
        )
        self.requirement_id = requirement_response.json()["id"]
        
        # Create a solution for testing
        solution_response = client.post(
            "/api/v1/solutions/",
            json={"title": "Test Solution", "description": "This is a test solution", "requirement_id": self.requirement_id}
        )
        self.solution_id = solution_response.json()["id"]
        
        # Create a development task for testing
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

    def test_create_application(self):
        response = client.post(
            "/api/v1/applications/",
            json={
                "name": "Test Application", 
                "description": "This is a test application", 
                "development_task_id": self.dev_task_id,
                "created_by": self.user_id
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Application")
        self.assertEqual(data["description"], "This is a test application")
        self.assertEqual(data["development_task_id"], self.dev_task_id)
        self.assertEqual(data["created_by"], self.user_id)

    def test_create_application_with_invalid_task(self):
        response = client.post(
            "/api/v1/applications/",
            json={
                "name": "Test Application", 
                "description": "This is a test application", 
                "development_task_id": 999,
                "created_by": self.user_id
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_create_application_with_invalid_user(self):
        response = client.post(
            "/api/v1/applications/",
            json={
                "name": "Test Application", 
                "description": "This is a test application", 
                "development_task_id": self.dev_task_id,
                "created_by": 999
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_get_applications(self):
        # First create an application
        client.post(
            "/api/v1/applications/",
            json={
                "name": "Test Application", 
                "description": "This is a test application", 
                "development_task_id": self.dev_task_id,
                "created_by": self.user_id
            }
        )
        
        # Then get all applications
        response = client.get("/api/v1/applications/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], "Test Application")

    def test_get_application(self):
        # First create an application
        create_response = client.post(
            "/api/v1/applications/",
            json={
                "name": "Test Application", 
                "description": "This is a test application", 
                "development_task_id": self.dev_task_id,
                "created_by": self.user_id
            }
        )
        application_id = create_response.json()["id"]
        
        # Then get the application
        response = client.get(f"/api/v1/applications/{application_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Test Application")

    def test_get_nonexistent_application(self):
        response = client.get("/api/v1/applications/999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()