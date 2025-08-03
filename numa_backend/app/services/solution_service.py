from sqlalchemy.orm import Session
from app.models.solution import Solution as SolutionModel
from app.schemas.solution import SolutionCreate

def create_solution(db: Session, solution: SolutionCreate):
    db_solution = SolutionModel(**solution.dict())
    db.add(db_solution)
    db.commit()
    db.refresh(db_solution)
    return db_solution

def get_solution(db: Session, solution_id: int):
    return db.query(SolutionModel).filter(SolutionModel.id == solution_id).first()

def get_solutions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SolutionModel).offset(skip).limit(limit).all()