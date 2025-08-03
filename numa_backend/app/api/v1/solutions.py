from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.solution import Solution, SolutionCreate
from app.services.solution_service import create_solution, get_solution, get_solutions
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Solution)
def create_new_solution(solution: SolutionCreate, db: Session = Depends(get_db)):
    return create_solution(db, solution)

@router.get("/{solution_id}", response_model=Solution)
def read_solution(solution_id: int, db: Session = Depends(get_db)):
    db_solution = get_solution(db, solution_id)
    if db_solution is None:
        raise HTTPException(status_code=404, detail="Solution not found")
    return db_solution

@router.get("/", response_model=List[Solution])
def read_solutions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_solutions(db, skip=skip, limit=limit)