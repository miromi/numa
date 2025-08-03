from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.deployment import Deployment, DeploymentCreate
from app.services.deployment_service import create_deployment, get_deployment, get_deployments
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Deployment)
def create_new_deployment(deployment: DeploymentCreate, db: Session = Depends(get_db)):
    return create_deployment(db, deployment)

@router.get("/{deployment_id}", response_model=Deployment)
def read_deployment(deployment_id: int, db: Session = Depends(get_db)):
    db_deployment = get_deployment(db, deployment_id)
    if db_deployment is None:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return db_deployment

@router.get("/", response_model=List[Deployment])
def read_deployments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_deployments(db, skip=skip, limit=limit)