# Numa Backend

This is the backend service for the Numa project, built with FastAPI.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```
   python scripts/init_db.py
   ```

3. Run the server:
   ```
   uvicorn main:app --reload
   ```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access the auto-generated API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc