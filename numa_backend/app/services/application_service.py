from sqlalchemy.orm import Session
from app.models.application import Application as ApplicationModel
from app.schemas.application import ApplicationCreate
from app.models.user import User as UserModel

def create_application(db: Session, application: ApplicationCreate):
    # Check if the creating user exists
    user = db.query(UserModel).filter(UserModel.id == application.created_by).first()
    if not user:
        raise ValueError("Creating user not found")
    
    # Validate required fields
    if not application.repository_url:
        raise ValueError("Repository URL is required")
    
    if not application.owner:
        raise ValueError("Owner is required")
    
    if not application.app_id:
        raise ValueError("App ID is required")
    
    # Check if name is unique
    existing_app = db.query(ApplicationModel).filter(ApplicationModel.name == application.name).first()
    if existing_app:
        raise ValueError("Application name must be unique")
    
    # Check if app_id is unique
    existing_app = db.query(ApplicationModel).filter(ApplicationModel.app_id == application.app_id).first()
    if existing_app:
        raise ValueError("App ID must be unique")
    
    # Check if repository_url is unique
    existing_app = db.query(ApplicationModel).filter(ApplicationModel.repository_url == application.repository_url).first()
    if existing_app:
        raise ValueError("Repository URL must be unique")
    
    # 调试输出，查看传入的字段值
    print(f"Creating application with: name={application.name}, owner={application.owner}, app_id={application.app_id}")
    
    db_application = ApplicationModel(**application.dict())
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_application(db: Session, application_id: int):
    return db.query(ApplicationModel).filter(ApplicationModel.id == application_id).first()

def get_application_by_app_id(db: Session, app_id: str):
    return db.query(ApplicationModel).filter(ApplicationModel.app_id == app_id).first()

def get_applications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(ApplicationModel).offset(skip).limit(limit).all()

def update_application_status(db: Session, application_id: int, status: str):
    db_application = get_application(db, application_id)
    if db_application:
        db_application.status = status
        db.commit()
        db.refresh(db_application)
    return db_application