from sqlalchemy.orm import Session
from app.models.solution_question import SolutionQuestion as SolutionQuestionModel
from app.models.solution import Solution as SolutionModel
from app.models.user import User as UserModel
from app.schemas.solution_question import SolutionQuestionCreate, SolutionQuestionUpdate
from app.services.event_log_service import create_event_log

def create_solution_question(db: Session, question: SolutionQuestionCreate, current_user_id: int):
    # 检查方案是否存在
    solution = db.query(SolutionModel).filter(SolutionModel.id == question.solution_id).first()
    if not solution:
        raise ValueError("方案未找到")
    
    # 检查用户是否存在
    user = db.query(UserModel).filter(UserModel.id == question.created_by).first()
    if not user:
        raise ValueError("用户未找到")
    
    # 创建问题
    db_question = SolutionQuestionModel(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    
    # 记录事件
    create_event_log(
        db,
        event_type="solution_question_created",
        description=f"用户 {user.name} 提出了问题: {question.content}",
        user_id=current_user_id,
        requirement_id=solution.requirement_id,
        question_id=db_question.id
    )
    
    return db_question

def get_solution_question(db: Session, question_id: int):
    return db.query(SolutionQuestionModel).filter(SolutionQuestionModel.id == question_id).first()

def get_solution_questions_by_solution(db: Session, solution_id: int):
    return db.query(SolutionQuestionModel).filter(SolutionQuestionModel.solution_id == solution_id).all()

def answer_solution_question(db: Session, question_id: int, answer: str, answered_by: int, current_user_id: int):
    # 检查问题是否存在
    db_question = get_solution_question(db, question_id)
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
        event_type="solution_question_answered",
        description=f"用户 {user.name} 回答了问题: {answer}",
        user_id=current_user_id,
        requirement_id=db.query(SolutionModel).filter(SolutionModel.id == db_question.solution_id).first().requirement_id,
        question_id=question_id
    )
    
    return db_question

def clarify_solution_question(db: Session, question_id: int, clarified_by: int, current_user_id: int):
    # 检查问题是否存在
    db_question = get_solution_question(db, question_id)
    if not db_question:
        raise ValueError("问题未找到")
    
    # 检查澄清用户是否存在
    user = db.query(UserModel).filter(UserModel.id == clarified_by).first()
    if not user:
        raise ValueError("澄清用户未找到")
    
    # 检查澄清用户是否为方案负责人
    solution = db.query(SolutionModel).filter(SolutionModel.id == db_question.solution_id).first()
    if not solution or solution.created_by != clarified_by:
        raise ValueError("只有方案负责人才能标记问题为已澄清")
    
    # 更新问题
    db_question.clarified = True
    db_question.clarified_by = clarified_by
    db.commit()
    db.refresh(db_question)
    
    # 记录事件
    create_event_log(
        db,
        event_type="solution_question_clarified",
        description=f"用户 {user.name} 标记问题为已澄清",
        user_id=current_user_id,
        requirement_id=solution.requirement_id,
        question_id=question_id
    )
    
    return db_question