from sqlalchemy.orm import Session
from app.models.deployment import Deployment as DeploymentModel
from app.schemas.deployment import DeploymentCreate

def create_deployment(db: Session, deployment: DeploymentCreate):
    db_deployment = DeploymentModel(**deployment.dict())
    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)
    return db_deployment

def get_deployment(db: Session, deployment_id: int):
    return db.query(DeploymentModel).filter(DeploymentModel.id == deployment_id).first()

def get_deployments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeploymentModel).offset(skip).limit(limit).all()