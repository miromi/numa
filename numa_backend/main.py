from fastapi import FastAPI
from app.api.api import api_router
from app.core.database import engine, Base
from app.models import base, requirement, solution, development, deployment, user

# Create database tables
base.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Numa Backend")

app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to Numa Backend"}