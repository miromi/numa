from sqlalchemy.orm import Session
from app.models.development import DevelopmentTask as DevelopmentTaskModel
from app.schemas.development import DevelopmentTaskCreate
from app.models.solution import Solution as SolutionModel
from app.models.user import User as UserModel

def create_development_task(db: Session, task: DevelopmentTaskCreate):
    # Check if the solution exists
    solution = db.query(SolutionModel).filter(SolutionModel.id == task.solution_id).first()
    if not solution:
        raise ValueError("Solution not found")
    
    # Check if the assigned user exists (if provided)
    if task.assigned_to:
        user = db.query(UserModel).filter(UserModel.id == task.assigned_to).first()
        if not user:
            raise ValueError("Assigned user not found")
    
    db_task = DevelopmentTaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_development_task(db: Session, task_id: int):
    return db.query(DevelopmentTaskModel).filter(DevelopmentTaskModel.id == task_id).first()

def get_development_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DevelopmentTaskModel).offset(skip).limit(limit).all()