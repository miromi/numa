#!/usr/bin/env python3
"""
Avatar MVP 完整功能测试脚本（使用本地仓库）
"""

import sys
import os
import time
import shutil
import subprocess

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avatar import Avatar

def create_mock_repo(repo_path):
    """创建一个模拟的Git仓库"""
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    os.makedirs(repo_path)
    
    # 初始化Git仓库
    subprocess.run(["git", "init"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo_path, check=True)
    
    # 创建一个初始提交
    with open(os.path.join(repo_path, "README.md"), "w") as f:
        f.write("# Test Repository\n\nThis is a test repository for Avatar MVP testing.")
    
    subprocess.run(["git", "add", "README.md"], cwd=repo_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo_path, check=True)
    
    # 创建开发分支
    try:
        subprocess.run(["git", "checkout", "-b", "feature/test-task"], cwd=repo_path, check=True)
    except subprocess.CalledProcessError:
        # 如果分支已存在，则直接切换到该分支
        subprocess.run(["git", "checkout", "feature/test-task"], cwd=repo_path, check=True)
    
    print(f"Created mock repository at {repo_path}")

def test_execute_task():
    """测试任务执行功能"""
    print("Testing task execution...")
    
    # 创建Avatar实例
    avatar = Avatar()
    
    # 创建测试工作区
    workspace_path = avatar.config.get("avatar.workspace", "./workspace")
    repos_path = os.path.join(workspace_path, "repos")
    repo_path = os.path.join(repos_path, "app_1")
    
    if os.path.exists(workspace_path):
        shutil.rmtree(workspace_path)
    os.makedirs(repos_path)
    
    # 创建模拟仓库
    create_mock_repo(repo_path)
    
    # 修改avatar的配置，使其指向本地仓库
    # 这里我们直接修改API服务返回的应用信息
    original_get_application = avatar.api_service.get_application
    
    def mock_get_application(app_id):
        app_data = original_get_application(app_id)
        if app_data:
            # 修改git_repo_url为本地仓库路径
            app_data["git_repo_url"] = repo_path
        return app_data
    
    avatar.api_service.get_application = mock_get_application
    
    # 执行任务1
    try:
        success = avatar.execute_task(1)
        print(f"Task execution result: {'Success' if success else 'Failed'}")
        
        # 检查是否有新提交
        result = subprocess.run(["git", "log", "--oneline"], cwd=repo_path, 
                               capture_output=True, text=True, check=True)
        print("Repository commits:")
        print(result.stdout)
    except Exception as e:
        print(f"Error executing task: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("Starting Avatar MVP full functionality test with local repository...")
    
    # 显示Avatar状态
    avatar = Avatar()
    status = avatar.get_status()
    print(f"Avatar Status: {status}")
    
    # 测试任务执行
    test_execute_task()
    
    print("Test completed!")

if __name__ == "__main__":
    main()