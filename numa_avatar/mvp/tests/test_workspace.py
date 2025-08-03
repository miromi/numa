import unittest
import os
import tempfile
import shutil
import json
from workspace import WorkspaceManager

class TestWorkspaceManager(unittest.TestCase):
    """测试工作区管理类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录作为工作区
        self.temp_dir = tempfile.mkdtemp(prefix="avatar_test_")
        self.workspace_path = os.path.join(self.temp_dir, "workspace")
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_init_workspace(self):
        """测试初始化工作区"""
        # 创建工作区管理器
        workspace = WorkspaceManager(self.workspace_path)
        
        # 验证目录是否创建
        self.assertTrue(os.path.exists(self.workspace_path))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_path, "repos")))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_path, "temp")))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_path, "logs")))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_path, "cache")))
        self.assertTrue(os.path.exists(os.path.join(self.workspace_path, "config")))
        
        # 验证workspace.json是否创建
        workspace_info_file = os.path.join(self.workspace_path, "workspace.json")
        self.assertTrue(os.path.exists(workspace_info_file))
        
        # 验证workspace.json内容
        with open(workspace_info_file, 'r') as f:
            info = json.load(f)
            self.assertIn("created_at", info)
            self.assertIn("version", info)
    
    def test_get_repo_path(self):
        """测试获取仓库路径"""
        workspace = WorkspaceManager(self.workspace_path)
        repo_path = workspace.get_repo_path("test_repo")
        
        expected_path = os.path.join(self.workspace_path, "repos", "test_repo")
        self.assertEqual(repo_path, expected_path)
    
    def test_get_temp_path(self):
        """测试获取临时路径"""
        workspace = WorkspaceManager(self.workspace_path)
        temp_path = workspace.get_temp_path("test_task")
        
        expected_path = os.path.join(self.workspace_path, "temp", "task_test_task")
        self.assertEqual(temp_path, expected_path)
        self.assertTrue(os.path.exists(temp_path))
    
    def test_get_log_file(self):
        """测试获取日志文件路径"""
        workspace = WorkspaceManager(self.workspace_path)
        
        # 测试获取主日志文件
        log_file = workspace.get_log_file()
        expected_path = os.path.join(self.workspace_path, "logs", "avatar.log")
        self.assertEqual(log_file, expected_path)
        
        # 测试获取任务日志文件
        task_log_file = workspace.get_log_file("test_task")
        expected_path = os.path.join(self.workspace_path, "logs", "task_logs", "task_test_task.log")
        self.assertEqual(task_log_file, expected_path)
        
        # 验证任务日志目录是否创建
        task_log_dir = os.path.join(self.workspace_path, "logs", "task_logs")
        self.assertTrue(os.path.exists(task_log_dir))
    
    def test_get_cache_file(self):
        """测试获取缓存文件路径"""
        workspace = WorkspaceManager(self.workspace_path)
        cache_file = workspace.get_cache_file("test_cache")
        
        expected_path = os.path.join(self.workspace_path, "cache", "test_cache.cache")
        self.assertEqual(cache_file, expected_path)
    
    def test_cleanup_temp(self):
        """测试清理临时文件"""
        workspace = WorkspaceManager(self.workspace_path)
        
        # 创建任务临时目录
        task_temp_path = workspace.get_temp_path("test_task")
        test_file = os.path.join(task_temp_path, "test.txt")
        with open(test_file, 'w') as f:
            f.write("test content")
        
        # 验证文件存在
        self.assertTrue(os.path.exists(test_file))
        
        # 清理特定任务临时文件
        workspace.cleanup_temp("test_task")
        
        # 验证任务临时目录已被删除
        self.assertFalse(os.path.exists(task_temp_path))
        
        # 重新创建临时目录进行整体清理测试
        task_temp_path1 = workspace.get_temp_path("test_task1")
        task_temp_path2 = workspace.get_temp_path("test_task2")
        
        self.assertTrue(os.path.exists(task_temp_path1))
        self.assertTrue(os.path.exists(task_temp_path2))
        
        # 清理所有临时文件
        workspace.cleanup_temp()
        
        # 验证所有临时目录已被删除
        self.assertFalse(os.path.exists(task_temp_path1))
        self.assertFalse(os.path.exists(task_temp_path2))
    
    def test_get_workspace_info(self):
        """测试获取工作区信息"""
        workspace = WorkspaceManager(self.workspace_path)
        info = workspace.get_workspace_info()
        
        self.assertIsInstance(info, dict)
        self.assertIn("created_at", info)
        self.assertIn("version", info)
    
    def test_is_valid_workspace(self):
        """测试验证工作区有效性"""
        # 未初始化的工作区
        invalid_workspace = WorkspaceManager(os.path.join(self.temp_dir, "invalid_workspace"))
        self.assertFalse(invalid_workspace.is_valid_workspace())
        
        # 已初始化的工作区
        valid_workspace = WorkspaceManager(self.workspace_path)
        self.assertTrue(valid_workspace.is_valid_workspace())

if __name__ == '__main__':
    unittest.main()