from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.development import DevelopmentTask, DevelopmentTaskCreate
from app.services.development_service import create_development_task, get_development_task, get_development_tasks
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=DevelopmentTask)
def create_new_development_task(task: DevelopmentTaskCreate, db: Session = Depends(get_db)):
    try:
        return create_development_task(db, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", response_model=DevelopmentTask)
def read_development_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_development_task(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Development task not found")
    return db_task

@router.get("/", response_model=List[DevelopmentTask])
def read_development_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_development_tasks(db, skip=skip, limit=limit)