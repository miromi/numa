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

class TestDevelopmentAPI(unittest.TestCase):
    def setUp(self):
        # Create a fresh database for each test
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        
        # Create a requirement for testing
        requirement_response = client.post(
            "/api/v1/requirements/",
            json={"title": "Test Requirement", "description": "This is a test requirement", "user_id": 1}
        )
        self.requirement_id = requirement_response.json()["id"]
        
        # Create a solution for testing
        solution_response = client.post(
            "/api/v1/solutions/",
            json={"title": "Test Solution", "description": "This is a test solution", "requirement_id": self.requirement_id}
        )
        self.solution_id = solution_response.json()["id"]
        
        # Create a user for testing
        user_response = client.post(
            "/api/v1/users/",
            json={"name": "Test User", "email": "test@example.com"}
        )
        self.user_id = user_response.json()["id"]

    def test_create_development_task(self):
        response = client.post(
            "/api/v1/development/",
            json={
                "title": "Test Development Task", 
                "description": "This is a test development task", 
                "solution_id": self.solution_id,
                "assigned_to": self.user_id
            }
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Development Task")
        self.assertEqual(data["description"], "This is a test development task")
        self.assertEqual(data["solution_id"], self.solution_id)
        self.assertEqual(data["assigned_to"], self.user_id)

    def test_create_development_task_with_invalid_solution(self):
        response = client.post(
            "/api/v1/development/",
            json={
                "title": "Test Development Task", 
                "description": "This is a test development task", 
                "solution_id": 999,
                "assigned_to": self.user_id
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_create_development_task_with_invalid_user(self):
        response = client.post(
            "/api/v1/development/",
            json={
                "title": "Test Development Task", 
                "description": "This is a test development task", 
                "solution_id": self.solution_id,
                "assigned_to": 999
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_get_development_tasks(self):
        # First create a development task
        client.post(
            "/api/v1/development/",
            json={
                "title": "Test Development Task", 
                "description": "This is a test development task", 
                "solution_id": self.solution_id,
                "assigned_to": self.user_id
            }
        )
        
        # Then get all development tasks
        response = client.get("/api/v1/development/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "Test Development Task")

    def test_get_development_task(self):
        # First create a development task
        create_response = client.post(
            "/api/v1/development/",
            json={
                "title": "Test Development Task", 
                "description": "This is a test development task", 
                "solution_id": self.solution_id,
                "assigned_to": self.user_id
            }
        )
        task_id = create_response.json()["id"]
        
        # Then get the development task
        response = client.get(f"/api/v1/development/{task_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Test Development Task")

    def test_get_nonexistent_development_task(self):
        response = client.get("/api/v1/development/999")
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()