from sqlalchemy.orm import Session
from app.models.solution import Solution as SolutionModel
from app.schemas.solution import SolutionCreate
from app.models.requirement import Requirement as RequirementModel

def create_solution(db: Session, solution: SolutionCreate):
    # Check if the requirement exists
    requirement = db.query(RequirementModel).filter(RequirementModel.id == solution.requirement_id).first()
    if not requirement:
        raise ValueError("Requirement not found")
    
    db_solution = SolutionModel(**solution.dict())
    db.add(db_solution)
    db.commit()
    db.refresh(db_solution)
    return db_solution

def get_solution(db: Session, solution_id: int):
    return db.query(SolutionModel).filter(SolutionModel.id == solution_id).first()

def get_solutions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SolutionModel).offset(skip).limit(limit).all()