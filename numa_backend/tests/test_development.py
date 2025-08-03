import pytest
import sys
import os
import uuid

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from app.models.development import DevelopmentTask as DevelopmentTaskModel
from app.models.solution import Solution as SolutionModel
from app.models.requirement import Requirement as RequirementModel
from app.models.application import Application as ApplicationModel

client = TestClient(app)

@pytest.fixture
def db():
    # 在测试中我们不直接使用数据库会话
    # 这里返回None或可以返回一个模拟的数据库会话
    return None

def generate_unique_name():
    """生成唯一的名称"""
    return f"test-app-{uuid.uuid4()}"

def generate_unique_repo_url():
    """生成唯一的仓库URL"""
    return f"https://github.com/example/test-app-{uuid.uuid4()}.git"

def generate_unique_app_id():
    """生成唯一的app_id"""
    return f"test-app-id-{uuid.uuid4()}"

def test_create_development_task():
    """测试创建开发任务"""
    # 先创建一个应用
    app_data = {
        "name": generate_unique_name(),
        "description": "测试应用",
        "repository_url": generate_unique_repo_url(),
        "owner": "测试用户",
        "app_id": generate_unique_app_id(),
        "created_by": 1
    }
    app_response = client.post("/api/v1/applications/", json=app_data)
    assert app_response.status_code == 200
    app_id = app_response.json()["id"]
    
    # 创建需求
    requirement_data = {
        "title": "测试创建开发任务的需求",
        "description": "用于测试创建开发任务",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试创建开发任务的方案",
        "description": "用于测试创建开发任务",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    sol_response = client.post("/api/v1/solutions/", json=solution_data)
    assert sol_response.status_code == 200
    solution_id = sol_response.json()["id"]
    
    # 创建开发任务
    task_data = {
        "title": "测试开发任务",
        "description": "这是一个测试开发任务",
        "solution_id": solution_id,
        "requirement_id": requirement_id,
        "application_id": app_id,
        "assigned_to": 1,
        "status": "todo",
        "code_branch": "dev-test-branch"
    }
    response = client.post("/api/v1/development/", json=task_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["solution_id"] == solution_id
    assert data["requirement_id"] == requirement_id
    assert data["application_id"] == app_id
    assert data["assigned_to"] == 1
    assert data["status"] == "todo"
    assert data["code_branch"] == "dev-test-branch"

def test_get_development_task():
    """测试获取单个开发任务"""
    # 先创建一个应用
    app_data = {
        "name": generate_unique_name(),
        "description": "测试应用",
        "repository_url": generate_unique_repo_url(),
        "owner": "测试用户",
        "app_id": generate_unique_app_id(),
        "created_by": 1
    }
    app_response = client.post("/api/v1/applications/", json=app_data)
    assert app_response.status_code == 200
    app_id = app_response.json()["id"]
    
    # 创建需求
    requirement_data = {
        "title": "测试获取开发任务的需求",
        "description": "用于测试获取单个开发任务",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试获取开发任务的方案",
        "description": "用于测试获取单个开发任务",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    sol_response = client.post("/api/v1/solutions/", json=solution_data)
    assert sol_response.status_code == 200
    solution_id = sol_response.json()["id"]
    
    # 创建开发任务
    task_data = {
        "title": "测试获取开发任务",
        "description": "用于测试获取单个开发任务",
        "solution_id": solution_id,
        "requirement_id": requirement_id,
        "application_id": app_id,
        "assigned_to": 1,
        "status": "todo"
    }
    create_response = client.post("/api/v1/development/", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()
    
    # 获取开发任务
    response = client.get(f"/api/v1/development/{created_task['id']}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == created_task["id"]
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["solution_id"] == solution_id
    assert data["requirement_id"] == requirement_id
    assert data["application_id"] == app_id
    assert data["solution"] is not None
    assert data["requirement"] is not None
    assert data["application"] is not None

def test_get_development_tasks():
    """测试获取开发任务列表"""
    # 先创建一个应用
    app_data = {
        "name": generate_unique_name(),
        "description": "测试应用",
        "repository_url": generate_unique_repo_url(),
        "owner": "测试用户",
        "app_id": generate_unique_app_id(),
        "created_by": 1
    }
    app_response = client.post("/api/v1/applications/", json=app_data)
    assert app_response.status_code == 200
    app_id = app_response.json()["id"]
    
    # 创建需求
    requirement_data = {
        "title": "测试获取开发任务列表的需求",
        "description": "用于测试获取开发任务列表",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试获取开发任务列表的方案",
        "description": "用于测试获取开发任务列表",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    sol_response = client.post("/api/v1/solutions/", json=solution_data)
    assert sol_response.status_code == 200
    solution_id = sol_response.json()["id"]
    
    # 创建多个开发任务
    for i in range(3):
        task_data = {
            "title": f"测试开发任务列表 {i+1}",
            "description": f"用于测试获取开发任务列表 {i+1}",
            "solution_id": solution_id,
            "requirement_id": requirement_id,
            "application_id": app_id,
            "assigned_to": 1,
            "status": "todo"
        }
        response = client.post("/api/v1/development/", json=task_data)
        assert response.status_code == 200
    
    # 获取开发任务列表
    response = client.get("/api/v1/development/")
    assert response.status_code == 200
    data = response.json()
    
    # 检查至少有3个开发任务（可能有之前创建的）
    assert len(data) >= 3
    
    # 检查刚创建的开发任务是否在列表中
    titles = [task["title"] for task in data]
    for i in range(3):
        assert f"测试开发任务列表 {i+1}" in titles

def test_update_development_task_status():
    """测试更新开发任务状态"""
    # 先创建一个应用
    app_data = {
        "name": generate_unique_name(),
        "description": "测试应用",
        "repository_url": generate_unique_repo_url(),
        "owner": "测试用户",
        "app_id": generate_unique_app_id(),
        "created_by": 1
    }
    app_response = client.post("/api/v1/applications/", json=app_data)
    assert app_response.status_code == 200
    app_id = app_response.json()["id"]
    
    # 创建需求
    requirement_data = {
        "title": "测试更新开发任务状态的需求",
        "description": "用于测试更新开发任务状态",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试更新开发任务状态的方案",
        "description": "用于测试更新开发任务状态",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    sol_response = client.post("/api/v1/solutions/", json=solution_data)
    assert sol_response.status_code == 200
    solution_id = sol_response.json()["id"]
    
    # 创建开发任务
    task_data = {
        "title": "测试更新开发任务状态",
        "description": "用于测试更新开发任务状态",
        "solution_id": solution_id,
        "requirement_id": requirement_id,
        "application_id": app_id,
        "assigned_to": 1,
        "status": "todo"
    }
    create_response = client.post("/api/v1/development/", json=task_data)
    assert create_response.status_code == 200
    created_task = create_response.json()
    
    # 更新开发任务状态为进行中
    update_data = {
        "title": "测试更新开发任务状态",
        "description": "用于测试更新开发任务状态",
        "status": "in_progress"
    }
    response = client.put(f"/api/v1/development/{created_task['id']}", json=update_data)
    assert response.status_code == 200
    updated_task = response.json()
    
    assert updated_task["status"] == "in_progress"