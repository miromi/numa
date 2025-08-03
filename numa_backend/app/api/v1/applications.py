from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.application import Application, ApplicationCreate
from app.services.application_service import create_application, get_application, get_applications
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Application)
def create_new_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    try:
        return create_application(db, application)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{application_id}", response_model=Application)
def read_application(application_id: int, db: Session = Depends(get_db)):
    db_application = get_application(db, application_id)
    if db_application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return db_application

@router.get("/", response_model=List[Application])
def read_applications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_applications(db, skip=skip, limit=limit)