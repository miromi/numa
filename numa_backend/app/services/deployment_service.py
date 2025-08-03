from sqlalchemy.orm import Session
from app.models.deployment import Deployment as DeploymentModel
from app.schemas.deployment import DeploymentCreate
from app.models.development import DevelopmentTask as DevelopmentTaskModel
from app.models.user import User as UserModel

def create_deployment(db: Session, deployment: DeploymentCreate):
    # Check if the development task exists
    task = db.query(DevelopmentTaskModel).filter(DevelopmentTaskModel.id == deployment.development_task_id).first()
    if not task:
        raise ValueError("Development task not found")
    
    # Check if the deploying user exists (if provided)
    if deployment.deployed_by:
        user = db.query(UserModel).filter(UserModel.id == deployment.deployed_by).first()
        if not user:
            raise ValueError("Deploying user not found")
    
    db_deployment = DeploymentModel(**deployment.dict())
    db.add(db_deployment)
    db.commit()
    db.refresh(db_deployment)
    return db_deployment

def get_deployment(db: Session, deployment_id: int):
    return db.query(DeploymentModel).filter(DeploymentModel.id == deployment_id).first()

def get_deployments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DeploymentModel).offset(skip).limit(limit).all()