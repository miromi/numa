#!/usr/bin/env python3
"""
Avatar MVP 测试脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avatar import Avatar

def main():
    """主函数"""
    print("Starting Avatar MVP...")
    
    # 创建Avatar实例
    avatar = Avatar()
    
    # 显示Avatar状态
    status = avatar.get_status()
    print(f"Avatar Status: {status}")
    
    # 注意：这里我们不调用avatar.start()，因为那会进入无限循环
    # 而是测试一些具体的功能
    
    # 测试获取任务（需要后端服务运行）
    print("\nTesting task retrieval...")
    try:
        # 这里使用一个假的任务ID进行测试
        task = avatar.get_task(1)
        if task:
            print(f"Task: {task}")
        else:
            print("Could not retrieve task. Make sure the backend service is running.")
    except Exception as e:
        print(f"Error retrieving task: {e}")

if __name__ == "__main__":
    main()