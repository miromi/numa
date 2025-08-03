import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from services.git_service import GitService
from utils.executor import CommandExecutor

class TestGitService(unittest.TestCase):
    """测试Git服务"""
    
    def setUp(self):
        """测试前准备"""
        self.git_service = GitService(username="testuser", email="test@example.com")
    
    @patch('services.git_service.CommandExecutor')
    def test_clone_repository(self, mock_executor):
        """测试克隆仓库功能"""
        # 设置模拟执行器返回值
        mock_executor.run_command.return_value = {"success": True, "stdout": "", "stderr": "", "returncode": 0}
        
        # 执行测试
        result = self.git_service.clone_repository("https://github.com/test/repo.git", "/tmp/test_repo")
        
        # 验证结果
        self.assertTrue(result)
        mock_executor.run_command.assert_called_once_with(["git", "clone", "https://github.com/test/repo.git", "/tmp/test_repo"])
    
    @patch('services.git_service.CommandExecutor')
    def test_checkout_branch_create_new(self, mock_executor):
        """测试创建并切换分支功能"""
        # 设置模拟执行器返回值
        mock_executor.run_command.return_value = {"success": True, "stdout": "", "stderr": "", "returncode": 0}
        
        # 执行测试
        result = self.git_service.checkout_branch("/tmp/test_repo", "feature-branch", create_new=True)
        
        # 验证结果
        self.assertTrue(result)
        mock_executor.run_command.assert_called_once_with(["git", "checkout", "-b", "feature-branch"], cwd="/tmp/test_repo")
    
    @patch('services.git_service.CommandExecutor')
    def test_checkout_branch_existing(self, mock_executor):
        """测试切换到现有分支功能"""
        # 设置模拟执行器返回值
        mock_executor.run_command.return_value = {"success": True, "stdout": "", "stderr": "", "returncode": 0}
        
        # 执行测试
        result = self.git_service.checkout_branch("/tmp/test_repo", "existing-branch", create_new=False)
        
        # 验证结果
        self.assertTrue(result)
        mock_executor.run_command.assert_called_once_with(["git", "checkout", "existing-branch"], cwd="/tmp/test_repo")
    
    @patch('services.git_service.CommandExecutor')
    def test_commit_changes_all_files(self, mock_executor):
        """测试提交所有文件变更"""
        # 设置模拟执行器返回值
        mock_executor.run_command.return_value = {"success": True, "stdout": "", "stderr": "", "returncode": 0}
        
        # 执行测试
        result = self.git_service.commit_changes("/tmp/test_repo", "Test commit message")
        
        # 验证结果
        self.assertTrue(result)
        # 验证调用顺序
        calls = mock_executor.run_command.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0][0], (["git", "add", "."],))
        self.assertEqual(calls[0][1], {"cwd": "/tmp/test_repo"})
        self.assertEqual(calls[1][0], (["git", "commit", "-m", "Test commit message"],))
        self.assertEqual(calls[1][1], {"cwd": "/tmp/test_repo"})
    
    @patch('services.git_service.CommandExecutor')
    def test_commit_changes_specific_files(self, mock_executor):
        """测试提交特定文件"""
        # 设置模拟执行器返回值
        mock_executor.run_command.return_value = {"success": True, "stdout": "", "stderr": "", "returncode": 0}
        
        # 执行测试
        result = self.git_service.commit_changes("/tmp/test_repo", "Test commit message", ["file1.txt", "file2.txt"])
        
        # 验证结果
        self.assertTrue(result)
        # 验证调用顺序
        calls = mock_executor.run_command.call_args_list
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0][0], (["git", "add", "file1.txt"],))
        self.assertEqual(calls[0][1], {"cwd": "/tmp/test_repo"})
        self.assertEqual(calls[1][0], (["git", "add", "file2.txt"],))
        self.assertEqual(calls[1][1], {"cwd": "/tmp/test_repo"})
        self.assertEqual(calls[2][0], (["git", "commit", "-m", "Test commit message"],))
        self.assertEqual(calls[2][1], {"cwd": "/tmp/test_repo"})
    
    @patch('services.git_service.CommandExecutor')
    def test_push_changes(self, mock_executor):
        """测试推送变更"""
        # 设置模拟执行器返回值
        mock_executor.run_command.return_value = {"success": True, "stdout": "", "stderr": "", "returncode": 0}
        
        # 执行测试
        result = self.git_service.push_changes("/tmp/test_repo", "feature-branch")
        
        # 验证结果
        self.assertTrue(result)
        mock_executor.run_command.assert_called_once_with(["git", "push", "origin", "feature-branch"], cwd="/tmp/test_repo")

if __name__ == '__main__':
    unittest.main()