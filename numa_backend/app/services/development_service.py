from sqlalchemy.orm import Session
from app.models.development import DevelopmentTask as DevelopmentTaskModel
from app.schemas.development import DevelopmentTaskCreate, DevelopmentTaskUpdate
from app.models.solution import Solution as SolutionModel
from app.models.requirement import Requirement as RequirementModel
from app.models.application import Application as ApplicationModel
from app.models.user import User as UserModel

def create_development_task(db: Session, task: DevelopmentTaskCreate):
    # Check if the solution exists
    solution = db.query(SolutionModel).filter(SolutionModel.id == task.solution_id).first()
    if not solution:
        raise ValueError("Solution not found")
    
    # Check if the assigned user exists (if provided)
    if task.assigned_to:
        user = db.query(UserModel).filter(UserModel.id == task.assigned_to).first()
        if not user:
            raise ValueError("Assigned user not found")
    
    db_task = DevelopmentTaskModel(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_development_task(db: Session, task_id: int):
    return db.query(DevelopmentTaskModel).filter(DevelopmentTaskModel.id == task_id).first()

def get_development_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(DevelopmentTaskModel).offset(skip).limit(limit).all()

def get_development_task_with_relations(db: Session, task_id: int):
    """获取开发任务及其关联信息"""
    db_task = db.query(DevelopmentTaskModel).filter(DevelopmentTaskModel.id == task_id).first()
    if db_task:
        # 获取关联的方案
        solution = db.query(SolutionModel).filter(SolutionModel.id == db_task.solution_id).first()
        db_task.solution = solution
        
        # 获取关联的需求
        requirement = db.query(RequirementModel).filter(RequirementModel.id == db_task.requirement_id).first()
        db_task.requirement = requirement
        
        # 获取关联的应用
        application = db.query(ApplicationModel).filter(ApplicationModel.id == db_task.application_id).first()
        db_task.application = application
            
    return db_task

def get_development_tasks_with_relations(db: Session, skip: int = 0, limit: int = 100):
    """获取开发任务列表及其关联信息"""
    tasks = db.query(DevelopmentTaskModel).offset(skip).limit(limit).all()
    for task in tasks:
        # 获取关联的方案
        solution = db.query(SolutionModel).filter(SolutionModel.id == task.solution_id).first()
        task.solution = solution
        
        # 获取关联的需求
        requirement = db.query(RequirementModel).filter(RequirementModel.id == task.requirement_id).first()
        task.requirement = requirement
        
        # 获取关联的应用
        application = db.query(ApplicationModel).filter(ApplicationModel.id == task.application_id).first()
        task.application = application
            
    return tasks

def update_development_task(db: Session, task_id: int, task_update: DevelopmentTaskUpdate):
    """更新开发任务"""
    db_task = get_development_task(db, task_id)
    if db_task:
        update_data = task_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

def create_development_task_from_solution(db: Session, solution: SolutionModel):
    """从方案创建开发任务"""
    # 获取方案关联的需求和应用
    requirement = db.query(RequirementModel).filter(RequirementModel.id == solution.requirement_id).first()
    application = db.query(ApplicationModel).filter(ApplicationModel.id == solution.application_id).first()
    
    if not requirement or not application:
        raise ValueError("关联的需求或应用未找到")
    
    # 生成代码分支名称
    branch_name = f"dev-{solution.id}-{solution.title.lower().replace(' ', '-')[:20]}"
    
    # 创建开发任务
    task_data = DevelopmentTaskCreate(
        title=f"开发任务 - {solution.title}",
        description=f"根据方案 '{solution.title}' 进行开发",
        solution_id=solution.id,
        requirement_id=solution.requirement_id,
        application_id=solution.application_id,
        assigned_to=solution.created_by,
        status="todo",
        code_branch=branch_name
    )
    
    db_task = DevelopmentTaskModel(**task_data.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task