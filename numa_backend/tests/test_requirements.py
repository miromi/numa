import pytest
import sys
import os
import uuid

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
from app.models.requirement import Requirement as RequirementModel
from app.models.application import Application as ApplicationModel
from app.schemas.requirement import RequirementCreate

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

def test_create_requirement():
    """测试创建需求"""
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
        "title": "测试需求",
        "description": "这是一个测试需求",
        "application_id": app_id,
        "user_id": 1
    }
    response = client.post("/api/v1/requirements/", json=requirement_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == requirement_data["title"]
    assert data["description"] == requirement_data["description"]
    assert data["application_id"] == app_id
    assert data["status"] == "pending"  # 需求创建后的默认状态是pending

def test_get_requirement():
    """测试获取单个需求"""
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
        "title": "测试获取需求",
        "description": "用于测试获取单个需求",
        "application_id": app_id,
        "user_id": 1
    }
    create_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert create_response.status_code == 200
    created_requirement = create_response.json()
    
    # 获取需求
    response = client.get(f"/api/v1/requirements/{created_requirement['id']}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == created_requirement["id"]
    assert data["title"] == requirement_data["title"]
    assert data["description"] == requirement_data["description"]
    assert data["application_id"] == app_id

def test_get_requirements():
    """测试获取需求列表"""
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
    
    # 创建多个需求
    for i in range(3):
        requirement_data = {
            "title": f"测试需求列表 {i+1}",
            "description": f"用于测试获取需求列表 {i+1}",
            "application_id": app_id,
            "user_id": 1
        }
        response = client.post("/api/v1/requirements/", json=requirement_data)
        assert response.status_code == 200
    
    # 获取需求列表
    response = client.get("/api/v1/requirements/")
    assert response.status_code == 200
    data = response.json()
    
    # 检查至少有3个需求（可能有之前创建的）
    assert len(data) >= 3
    
    # 检查刚创建的需求是否在列表中
    titles = [req["title"] for req in data]
    for i in range(3):
        assert f"测试需求列表 {i+1}" in titles

def test_update_requirement_status():
    """测试更新需求状态"""
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
        "title": "测试更新需求状态",
        "description": "用于测试更新需求状态",
        "application_id": app_id,
        "user_id": 1
    }
    create_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert create_response.status_code == 200
    created_requirement = create_response.json()
    
    # 更新需求状态为已接手
    update_data = {"status": "taken"}
    response = client.put(f"/api/v1/requirements/{created_requirement['id']}", json=update_data)
    assert response.status_code == 200
    updated_requirement = response.json()
    
    assert updated_requirement["status"] == "taken"

def test_confirm_requirement():
    """测试确认需求"""
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
        "title": "测试确认需求",
        "description": "用于测试确认需求",
        "application_id": app_id,
        "user_id": 1
    }
    create_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert create_response.status_code == 200
    created_requirement = create_response.json()
    
    # 确认需求
    response = client.post(f"/api/v1/requirements/{created_requirement['id']}/confirm")
    assert response.status_code == 200
    confirmed_requirement = response.json()
    
    assert confirmed_requirement["status"] == "confirmed"

def test_complete_requirement():
    """测试完成需求"""
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
        "title": "测试完成需求",
        "description": "用于测试完成需求",
        "application_id": app_id,
        "user_id": 1
    }
    create_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert create_response.status_code == 200
    created_requirement = create_response.json()
    
    # 完成需求
    response = client.post(f"/api/v1/requirements/{created_requirement['id']}/complete")
    assert response.status_code == 200
    completed_requirement = response.json()
    
    assert completed_requirement["status"] == "completed"