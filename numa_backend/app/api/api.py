from fastapi import APIRouter

from app.api.v1 import requirements, solutions, development, deployment, users, applications, questions, event_logs

api_router = APIRouter()
api_router.include_router(requirements.router, prefix="/v1/requirements", tags=["requirements"])
api_router.include_router(solutions.router, prefix="/v1/solutions", tags=["solutions"])
api_router.include_router(development.router, prefix="/v1/development", tags=["development"])
api_router.include_router(deployment.router, prefix="/v1/deployment", tags=["deployment"])
api_router.include_router(users.router, prefix="/v1/users", tags=["users"])
api_router.include_router(applications.router, prefix="/v1/applications", tags=["applications"])
api_router.include_router(questions.router, prefix="/v1/questions", tags=["questions"])
api_router.include_router(event_logs.router, prefix="/v1/event_logs", tags=["event_logs"])