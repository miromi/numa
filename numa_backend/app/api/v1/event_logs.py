from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.event_log import EventLog
from app.services.event_log_service import get_event_logs, get_event_logs_by_requirement, get_event_logs_by_question
from app.core.dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[EventLog])
def read_event_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_event_logs(db, skip=skip, limit=limit)

@router.get("/requirement/{requirement_id}", response_model=List[EventLog])
def read_event_logs_by_requirement(requirement_id: int, db: Session = Depends(get_db)):
    return get_event_logs_by_requirement(db, requirement_id)

@router.get("/question/{question_id}", response_model=List[EventLog])
def read_event_logs_by_question(question_id: int, db: Session = Depends(get_db)):
    return get_event_logs_by_question(db, question_id)