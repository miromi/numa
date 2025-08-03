from sqlalchemy.orm import Session
from app.models.development import DevelopmentTask as DevelopmentTaskModel
from app.schemas.development import DevelopmentTaskCreate

def create_development_task(db: Session, task: DevelopmentTaskCreate):
    db_task = DevelopmentTaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_development_task(db: Session, task_id: int):
    return db.query(DevelopmentTaskModel).filter(DevelopmentTaskModel.id == task_id).first()

def get_development_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DevelopmentTaskModel).offset(skip).limit(limit).all()