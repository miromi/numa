from sqlalchemy.orm import Session
from app.models.question import Question as QuestionModel
from app.models.requirement import Requirement as RequirementModel
from app.models.user import User as UserModel
from app.schemas.question import QuestionCreate, QuestionUpdate
from app.services.event_log_service import create_event_log

def create_question(db: Session, question: QuestionCreate, current_user_id: int):
    # 检查需求是否存在
    requirement = db.query(RequirementModel).filter(RequirementModel.id == question.requirement_id).first()
    if not requirement:
        raise ValueError("需求未找到")
    
    # 检查用户是否存在
    user = db.query(UserModel).filter(UserModel.id == question.created_by).first()
    if not user:
        raise ValueError("用户未找到")
    
    # 创建问题
    db_question = QuestionModel(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    # 记录事件
    create_event_log(
        db,
        event_type="question_created",
        description=f"用户 {user.name} 提出了问题: {question.content}",
        user_id=current_user_id,
        requirement_id=question.requirement_id,
        question_id=db_question.id
    )
    
    return db_question

def get_question(db: Session, question_id: int):
    return db.query(QuestionModel).filter(QuestionModel.id == question_id).first()

def get_questions_by_requirement(db: Session, requirement_id: int):
    return db.query(QuestionModel).filter(QuestionModel.requirement_id == requirement_id).all()

def answer_question(db: Session, question_id: int, answer: str, answered_by: int, current_user_id: int):
    # 检查问题是否存在
    db_question = get_question(db, question_id)
    if not db_question:
        raise ValueError("问题未找到")
    
    # 检查回答用户是否存在
    user = db.query(UserModel).filter(UserModel.id == answered_by).first()
    if not user:
        raise ValueError("回答用户未找到")
    
    # 更新问题
    db_question.answer = answer
    db_question.answered_by = answered_by
    db.commit()
    db.refresh(db_question)
    
    # 记录事件
    create_event_log(
        db,
        event_type="question_answered",
        description=f"用户 {user.name} 回答了问题: {answer}",
        user_id=current_user_id,
        requirement_id=db_question.requirement_id,
        question_id=question_id
    )
    
    return db_question

def clarify_question(db: Session, question_id: int, clarified_by: int, current_user_id: int):
    # 检查问题是否存在
    db_question = get_question(db, question_id)
    if not db_question:
        raise ValueError("问题未找到")
    
    # 检查澄清用户是否存在
    user = db.query(UserModel).filter(UserModel.id == clarified_by).first()
    if not user:
        raise ValueError("澄清用户未找到")
    
    # 检查澄清用户是否为需求接手人
    requirement = db.query(RequirementModel).filter(RequirementModel.id == db_question.requirement_id).first()
    if not requirement or requirement.assigned_to != clarified_by:
        raise ValueError("只有需求接手人才能标记问题为已澄清")
    
    # 更新问题
    db_question.clarified = True
    db_question.clarified_by = clarified_by
    db.commit()
    db.refresh(db_question)
    
    # 记录事件
    create_event_log(
        db,
        event_type="question_clarified",
        description=f"用户 {user.name} 标记问题为已澄清",
        user_id=current_user_id,
        requirement_id=db_question.requirement_id,
        question_id=question_id
    )
    
    return db_question

def check_all_questions_clarified(db: Session, requirement_id: int):
    """检查需求的所有问题是否都已澄清"""
    questions = get_questions_by_requirement(db, requirement_id)
    return all(question.clarified for question in questions) if questions else True