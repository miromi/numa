from fastapi import APIRouter

from app.api.v1 import requirements, solutions, development, deployment, users

api_router = APIRouter()
api_router.include_router(requirements.router, prefix="/v1/requirements", tags=["requirements"])
api_router.include_router(solutions.router, prefix="/v1/solutions", tags=["solutions"])
api_router.include_router(development.router, prefix="/v1/development", tags=["development"])
api_router.include_router(deployment.router, prefix="/v1/deployment", tags=["deployment"])
api_router.include_router(users.router, prefix="/v1/users", tags=["users"])