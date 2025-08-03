from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.requirement import Requirement, RequirementCreate, RequirementUpdate
from app.services.requirement_service import (
    create_requirement, get_requirement, get_requirements, 
    update_requirement, update_requirement_status, assign_requirement,
    confirm_requirement, generate_branch_name, generate_spec_document, clarify_requirement
)
from app.core.dependencies import get_db

router = APIRouter()

@router.post("/", response_model=Requirement)
def create_new_requirement(requirement: RequirementCreate, db: Session = Depends(get_db)):
    try:
        return create_requirement(db, requirement)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{requirement_id}", response_model=Requirement)
def read_requirement(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = get_requirement(db, requirement_id)
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return db_requirement

@router.get("/", response_model=List[Requirement])
def read_requirements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_requirements(db, skip=skip, limit=limit)

@router.put("/{requirement_id}", response_model=Requirement)
def update_requirement_endpoint(requirement_id: int, requirement_update: RequirementUpdate, db: Session = Depends(get_db)):
    db_requirement = update_requirement(db, requirement_id, requirement_update)
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return db_requirement

@router.patch("/{requirement_id}/status", response_model=Requirement)
def update_requirement_status_endpoint(requirement_id: int, status: str, db: Session = Depends(get_db)):
    db_requirement = update_requirement_status(db, requirement_id, status)
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return db_requirement

@router.post("/{requirement_id}/assign", response_model=Requirement)
def assign_requirement_endpoint(requirement_id: int, assigned_to: int, db: Session = Depends(get_db)):
    try:
        # 生成分支名称
        requirement = get_requirement(db, requirement_id)
        if not requirement:
            raise HTTPException(status_code=404, detail="Requirement not found")
        
        branch_name = generate_branch_name(requirement_id, requirement.title)
        
        # 生成需求规范文档
        spec_document = generate_spec_document(db, requirement_id)
        
        # 分配需求并更新相关信息
        db_requirement = assign_requirement(db, requirement_id, assigned_to)
        if db_requirement is None:
            raise HTTPException(status_code=404, detail="Requirement not found")
        
        # 更新分支名称和规范文档
        db_requirement = update_requirement(
            db, 
            requirement_id, 
            RequirementUpdate(branch_name=branch_name, spec_document=spec_document)
        )
        
        return db_requirement
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{requirement_id}/confirm", response_model=Requirement)
def confirm_requirement_endpoint(requirement_id: int, db: Session = Depends(get_db)):
    db_requirement = confirm_requirement(db, requirement_id)
    if db_requirement is None:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return db_requirement

@router.patch("/{requirement_id}/clarify", response_model=Requirement)
def clarify_requirement_endpoint(requirement_id: int, clarified: bool = True, db: Session = Depends(get_db)):
    try:
        db_requirement = clarify_requirement(db, requirement_id, clarified)
        return db_requirement
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))