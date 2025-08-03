from app.core.database import engine
from app.models import base, requirement, solution, development, deployment, user

def init_db():
    base.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")