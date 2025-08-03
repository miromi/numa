import pytest
import sys
import os
import uuid

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app
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

def test_create_solution():
    """测试创建方案"""
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
        "title": "测试创建方案的需求",
        "description": "用于测试创建方案",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试方案",
        "description": "这是一个测试方案",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    response = client.post("/api/v1/solutions/", json=solution_data)
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == solution_data["title"]
    assert data["description"] == solution_data["description"]
    assert data["requirement_id"] == requirement_id
    assert data["application_id"] == app_id
    assert data["status"] == "clarifying"  # 方案创建后的默认状态是clarifying

def test_get_solution():
    """测试获取单个方案"""
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
        "title": "测试获取方案的需求",
        "description": "用于测试获取单个方案",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试获取方案",
        "description": "用于测试获取单个方案",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    create_response = client.post("/api/v1/solutions/", json=solution_data)
    assert create_response.status_code == 200
    created_solution = create_response.json()
    
    # 获取方案
    response = client.get(f"/api/v1/solutions/{created_solution['id']}")
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == created_solution["id"]
    assert data["title"] == solution_data["title"]
    assert data["description"] == solution_data["description"]
    assert data["requirement_id"] == requirement_id
    assert data["application_id"] == app_id

def test_get_solutions():
    """测试获取方案列表"""
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
        "title": "测试获取方案列表的需求",
        "description": "用于测试获取方案列表",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建多个方案
    for i in range(3):
        solution_data = {
            "title": f"测试方案列表 {i+1}",
            "description": f"用于测试获取方案列表 {i+1}",
            "requirement_id": requirement_id,
            "application_id": app_id,
            "created_by": 1
        }
        response = client.post("/api/v1/solutions/", json=solution_data)
        assert response.status_code == 200
    
    # 获取方案列表
    response = client.get("/api/v1/solutions/")
    assert response.status_code == 200
    data = response.json()
    
    # 检查至少有3个方案（可能有之前创建的）
    assert len(data) >= 3
    
    # 检查刚创建的方案是否在列表中
    titles = [sol["title"] for sol in data]
    for i in range(3):
        assert f"测试方案列表 {i+1}" in titles

def test_update_solution_status():
    """测试更新方案状态"""
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
        "title": "测试更新方案状态的需求",
        "description": "用于测试更新方案状态",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试更新方案状态",
        "description": "用于测试更新方案状态",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    create_response = client.post("/api/v1/solutions/", json=solution_data)
    assert create_response.status_code == 200
    created_solution = create_response.json()
    
    # 更新方案状态为已接手
    update_data = {"status": "taken"}
    response = client.put(f"/api/v1/solutions/{created_solution['id']}", json=update_data)
    assert response.status_code == 200
    updated_solution = response.json()
    
    assert updated_solution["status"] == "taken"

def test_confirm_solution():
    """测试确认方案"""
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
        "title": "测试确认方案的需求",
        "description": "用于测试确认方案",
        "application_id": app_id,
        "user_id": 1
    }
    req_response = client.post("/api/v1/requirements/", json=requirement_data)
    assert req_response.status_code == 200
    requirement_id = req_response.json()["id"]
    
    # 创建方案
    solution_data = {
        "title": "测试确认方案",
        "description": "用于测试确认方案",
        "requirement_id": requirement_id,
        "application_id": app_id,
        "created_by": 1
    }
    create_response = client.post("/api/v1/solutions/", json=solution_data)
    assert create_response.status_code == 200
    created_solution = create_response.json()
    
    # 确认方案
    response = client.patch(f"/api/v1/solutions/{created_solution['id']}/confirm")
    assert response.status_code == 200
    confirmed_solution = response.json()
    
    assert confirmed_solution["status"] == "confirmed"

# 澄清方案的测试需要创建问题，暂时跳过
# def test_clarify_solution():
#     """测试澄清方案"""
#     # 先创建一个应用
#     app_data = {
#         "name": generate_unique_name(),
#         "description": "测试应用",
#         "repository_url": generate_unique_repo_url(),
#         "owner": "测试用户",
#         "app_id": generate_unique_app_id(),
#         "created_by": 1
#     }
#     app_response = client.post("/api/v1/applications/", json=app_data)
#     assert app_response.status_code == 200
#     app_id = app_response.json()["id"]
#     
#     # 创建需求
#     requirement_data = {
#         "title": "测试澄清方案的需求",
#         "description": "用于测试澄清方案",
#         "application_id": app_id,
#         "user_id": 1
#     }
#     req_response = client.post("/api/v1/requirements/", json=requirement_data)
#     assert req_response.status_code == 200
#     requirement_id = req_response.json()["id"]
#     
#     # 创建方案
#     solution_data = {
#         "title": "测试澄清方案",
#         "description": "用于测试澄清方案",
#         "requirement_id": requirement_id,
#         "application_id": app_id,
#         "created_by": 1
#     }
#     create_response = client.post("/api/v1/solutions/", json=solution_data)
#     assert create_response.status_code == 200
#     created_solution = create_response.json()
#     
#     # 创建问题
#     question_data = {
#         "solution_id": created_solution["id"],
#         "question": "这是一个测试问题",
#         "asked_by": 1
#     }
#     question_response = client.post("/api/v1/solutions/questions/", json=question_data)
#     assert question_response.status_code == 200
#     created_question = question_response.json()
#     
#     # 澄清问题
#     response = client.patch(f"/api/v1/solutions/questions/{created_question['id']}/clarify", 
#                            json={"clarified_by": 1})
#     assert response.status_code == 200
#     clarified_question = response.json()
#     
#     assert clarified_question["clarified"] == True