#!/usr/bin/env python3
"""
运行所有测试用例的脚本
"""

import unittest
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """运行所有测试"""
    print("Discovering and running tests...")
    
    # 发现并运行所有测试
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    
    # 根据测试结果设置退出码
    sys.exit(0 if success else 1)