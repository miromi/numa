from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.schemas.user import UserCreate

def create_user(db: Session, user: UserCreate):
    # Check if a user with the same email already exists
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise ValueError("A user with this email already exists")
    
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserModel).offset(skip).limit(limit).all()