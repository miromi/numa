from sqlalchemy.orm import Session
from app.models.solution import Solution as SolutionModel
from app.models.solution_question import SolutionQuestion as SolutionQuestionModel
from app.schemas.solution import SolutionCreate, SolutionUpdate
from app.models.requirement import Requirement as RequirementModel
from app.models.application import Application as ApplicationModel
from app.models.user import User as UserModel
from app.services.event_log_service import create_event_log

def create_solution(db: Session, solution: SolutionCreate):
    # Check if the requirement exists
    requirement = db.query(RequirementModel).filter(RequirementModel.id == solution.requirement_id).first()
    if not requirement:
        raise ValueError("Requirement not found")
    
    # Check if the application exists
    application = db.query(ApplicationModel).filter(ApplicationModel.id == solution.application_id).first()
    if not application:
        raise ValueError("Application not found")
    
    # Check if the user exists
    user = db.query(UserModel).filter(UserModel.id == solution.created_by).first()
    if not user:
        raise ValueError("User not found")
    
    db_solution = SolutionModel(**solution.dict())
    db.add(db_solution)
    db.commit()
    db.refresh(db_solution)
    
    # 记录事件
    create_event_log(
        db,
        event_type="solution_created",
        description=f"用户 {user.name} 创建了方案: {solution.title}",
        user_id=solution.created_by,
        requirement_id=solution.requirement_id
    )
    
    return db_solution

def get_solution(db: Session, solution_id: int):
    return db.query(SolutionModel).filter(SolutionModel.id == solution_id).first()

def get_solutions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SolutionModel).offset(skip).limit(limit).all()

def get_solutions_by_requirement(db: Session, requirement_id: int):
    return db.query(SolutionModel).filter(SolutionModel.requirement_id == requirement_id).all()

def update_solution(db: Session, solution_id: int, solution_update: SolutionUpdate):
    db_solution = get_solution(db, solution_id)
    if db_solution:
        update_data = solution_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_solution, key, value)
        db.commit()
        db.refresh(db_solution)
    return db_solution

def confirm_solution(db: Session, solution_id: int, confirmed: bool = True):
    """确认方案"""
    db_solution = get_solution(db, solution_id)
    if not db_solution:
        raise ValueError("方案未找到")
    
    # 检查是否所有问题都已澄清
    questions = db.query(SolutionQuestionModel).filter(SolutionQuestionModel.solution_id == solution_id).all()
    if confirmed and not all(question.clarified for question in questions):
        raise ValueError("还有未澄清的问题，请先澄清所有问题")
    
    # 更新方案
    db_solution.status = "confirmed" if confirmed else "clarifying"
    db_solution.clarified = confirmed
    db.commit()
    db.refresh(db_solution)
    
    # 如果方案被确认，创建开发任务
    if confirmed:
        from app.services.development_service import create_development_task_from_solution
        create_development_task_from_solution(db, db_solution)
    
    return db_solution

def get_solution_with_relations(db: Session, solution_id: int):
    """获取方案及其关联信息"""
    db_solution = db.query(SolutionModel).filter(SolutionModel.id == solution_id).first()
    if db_solution:
        # 获取关联的需求
        requirement = db.query(RequirementModel).filter(RequirementModel.id == db_solution.requirement_id).first()
        db_solution.requirement = requirement
        
        # 获取关联的应用
        if db_solution.application_id:
            application = db.query(ApplicationModel).filter(ApplicationModel.id == db_solution.application_id).first()
            db_solution.application = application
            
    return db_solution

def get_solutions_with_relations(db: Session, skip: int = 0, limit: int = 100):
    """获取方案列表及其关联信息"""
    solutions = db.query(SolutionModel).offset(skip).limit(limit).all()
    for solution in solutions:
        # 获取关联的需求
        requirement = db.query(RequirementModel).filter(RequirementModel.id == solution.requirement_id).first()
        solution.requirement = requirement
        
        # 获取关联的应用
        if solution.application_id:
            application = db.query(ApplicationModel).filter(ApplicationModel.id == solution.application_id).first()
            solution.application = application
            
    return solutions