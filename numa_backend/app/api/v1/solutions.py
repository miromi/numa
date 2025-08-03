from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.solution import Solution, SolutionCreate, SolutionUpdate
from app.schemas.solution_question import SolutionQuestion, SolutionQuestionCreate, SolutionQuestionUpdate
from app.services.solution_service import (
    create_solution, get_solution, get_solutions, get_solutions_by_requirement, 
    update_solution, confirm_solution, get_solution_with_relations, get_solutions_with_relations
)
from app.services.solution_question_service import (
    create_solution_question, get_solution_question, get_solution_questions_by_solution, 
    answer_solution_question, clarify_solution_question
)
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Solution)
def create_new_solution(solution: SolutionCreate, db: Session = Depends(get_db)):
    try:
        return create_solution(db, solution)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{solution_id}", response_model=Solution)
def read_solution(solution_id: int, db: Session = Depends(get_db)):
    db_solution = get_solution_with_relations(db, solution_id)
    if db_solution is None:
        raise HTTPException(status_code=404, detail="方案未找到")
    return db_solution

@router.get("/", response_model=List[Solution])
def read_solutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_solutions_with_relations(db, skip=skip, limit=limit)

@router.get("/requirement/{requirement_id}", response_model=List[Solution])
def read_solutions_by_requirement(requirement_id: int, db: Session = Depends(get_db)):
    solutions = get_solutions_by_requirement(db, requirement_id)
    # 为每个方案添加关联信息
    for solution in solutions:
        # 获取关联的需求
        from app.models.requirement import Requirement as RequirementModel
        requirement = db.query(RequirementModel).filter(RequirementModel.id == solution.requirement_id).first()
        solution.requirement = requirement
        
        # 获取关联的应用
        if solution.application_id:
            from app.models.application import Application as ApplicationModel
            application = db.query(ApplicationModel).filter(ApplicationModel.id == solution.application_id).first()
            solution.application = application
            
    return solutions

@router.put("/{solution_id}", response_model=Solution)
def update_solution_endpoint(solution_id: int, solution_update: SolutionUpdate, db: Session = Depends(get_db)):
    db_solution = update_solution(db, solution_id, solution_update)
    if db_solution is None:
        raise HTTPException(status_code=404, detail="方案未找到")
    return db_solution

@router.patch("/{solution_id}/confirm", response_model=Solution)
def confirm_solution_endpoint(solution_id: int, confirmed: bool = True, db: Session = Depends(get_db)):
    try:
        db_solution = confirm_solution(db, solution_id, confirmed)
        return db_solution
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 方案问题相关路由
@router.post("/questions/", response_model=SolutionQuestion)
def create_new_solution_question(question: SolutionQuestionCreate, current_user_id: int, db: Session = Depends(get_db)):
    try:
        return create_solution_question(db, question, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/questions/{question_id}", response_model=SolutionQuestion)
def read_solution_question(question_id: int, db: Session = Depends(get_db)):
    db_question = get_solution_question(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="问题未找到")
    return db_question

@router.get("/questions/solution/{solution_id}", response_model=List[SolutionQuestion])
def read_solution_questions_by_solution(solution_id: int, db: Session = Depends(get_db)):
    return get_solution_questions_by_solution(db, solution_id)

@router.patch("/questions/{question_id}/answer", response_model=SolutionQuestion)
def answer_solution_question_endpoint(question_id: int, answer: str, answered_by: int, current_user_id: int, db: Session = Depends(get_db)):
    try:
        return answer_solution_question(db, question_id, answer, answered_by, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/questions/{question_id}/clarify", response_model=SolutionQuestion)
def clarify_solution_question_endpoint(question_id: int, clarified_by: int, current_user_id: int, db: Session = Depends(get_db)):
    try:
        return clarify_solution_question(db, question_id, clarified_by, current_user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))