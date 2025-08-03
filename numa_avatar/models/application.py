from pydantic import BaseModel
from typing import Optional

class Application(BaseModel):
    """应用模型"""
    id: int
    name: str
    description: str
    git_repo_url: str
    owner: str