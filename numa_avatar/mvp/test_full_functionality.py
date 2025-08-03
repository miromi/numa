#!/usr/bin/env python3
"""
Avatar MVP 完整功能测试脚本
"""

import sys
import os
import time
import shutil

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avatar import Avatar

def test_execute_task():
    """测试任务执行功能"""
    print("Testing task execution...")
    
    # 创建Avatar实例
    avatar = Avatar()
    
    # 创建测试工作区
    workspace_path = avatar.config.get("avatar.workspace", "./workspace")
    if os.path.exists(workspace_path):
        shutil.rmtree(workspace_path)
    os.makedirs(workspace_path)
    
    # 执行任务1
    try:
        success = avatar.execute_task(1)
        print(f"Task execution result: {'Success' if success else 'Failed'}")
    except Exception as e:
        print(f"Error executing task: {e}")
        import traceback
        traceback.print_exc()

def main():
    """主函数"""
    print("Starting Avatar MVP full functionality test...")
    
    # 显示Avatar状态
    avatar = Avatar()
    status = avatar.get_status()
    print(f"Avatar Status: {status}")
    
    # 测试任务执行
    test_execute_task()
    
    print("Test completed!")

if __name__ == "__main__":
    main()