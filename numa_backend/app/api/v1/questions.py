from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.question import Question, QuestionCreate, QuestionUpdate
from app.services.question_service import create_question, get_question, get_questions_by_requirement, answer_question, clarify_question
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Question)
def create_new_question(question: QuestionCreate, current_user_id: int, db: Session = Depends(get_db)):
    try:
        return create_question(db, question, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{question_id}", response_model=Question)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = get_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="问题未找到")
    return db_question

@router.get("/requirement/{requirement_id}", response_model=List[Question])
def read_questions_by_requirement(requirement_id: int, db: Session = Depends(get_db)):
    return get_questions_by_requirement(db, requirement_id)

@router.patch("/{question_id}/answer", response_model=Question)
def answer_question_endpoint(question_id: int, answer: str, answered_by: int, current_user_id: int, db: Session = Depends(get_db)):
    try:
        return answer_question(db, question_id, answer, answered_by, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{question_id}/clarify", response_model=Question)
def clarify_question_endpoint(question_id: int, clarified_by: int, current_user_id: int, db: Session = Depends(get_db)):
    try:
        return clarify_question(db, question_id, clarified_by, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))