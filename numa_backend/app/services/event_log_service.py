from sqlalchemy.orm import Session
from app.models.event_log import EventLog as EventLogModel
from app.models.user import User as UserModel
from app.models.requirement import Requirement as RequirementModel
from app.models.question import Question as QuestionModel
from app.schemas.event_log import EventLogCreate

def create_event_log(db: Session, event_type: str, description: str, user_id: int, 
                     requirement_id: int = None, question_id: int = None):
    # 检查用户是否存在
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise ValueError("用户未找到")
    
    # 检查需求是否存在（如果提供了需求ID）
    if requirement_id:
        requirement = db.query(RequirementModel).filter(RequirementModel.id == requirement_id).first()
        if not requirement:
            raise ValueError("需求未找到")
    
    # 检查问题是否存在（如果提供了问题ID）
    if question_id:
        question = db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
        if not question:
            raise ValueError("问题未找到")
    
    # 创建事件记录
    event_log = EventLogCreate(
        event_type=event_type,
        description=description,
        user_id=user_id,
        requirement_id=requirement_id,
        question_id=question_id
    )
    
    db_event_log = EventLogModel(**event_log.dict())
    db.add(db_event_log)
    db.commit()
    db.refresh(db_event_log)
    
    return db_event_log

def get_event_logs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EventLogModel).offset(skip).limit(limit).all()

def get_event_logs_by_requirement(db: Session, requirement_id: int):
    return db.query(EventLogModel).filter(EventLogModel.requirement_id == requirement_id).all()

def get_event_logs_by_question(db: Session, question_id: int):
    return db.query(EventLogModel).filter(EventLogModel.question_id == question_id).all()