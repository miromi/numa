from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.development import DevelopmentTask, DevelopmentTaskCreate, DevelopmentTaskUpdate
from app.services.development_service import (
    create_development_task, get_development_task, get_development_tasks,
    get_development_task_with_relations, get_development_tasks_with_relations,
    update_development_task
)
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=DevelopmentTask)
def create_task(task: DevelopmentTaskCreate, db: Session = Depends(get_db)):
    try:
        return create_development_task(db, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{task_id}", response_model=DevelopmentTask)
def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = get_development_task_with_relations(db, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="开发任务未找到")
    return db_task

@router.get("/", response_model=List[DevelopmentTask])
def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_development_tasks_with_relations(db, skip=skip, limit=limit)

@router.put("/{task_id}", response_model=DevelopmentTask)
def update_task(task_id: int, task_update: DevelopmentTaskUpdate, db: Session = Depends(get_db)):
    db_task = update_development_task(db, task_id, task_update)
    if db_task is None:
        raise HTTPException(status_code=404, detail="开发任务未找到")
    return db_task