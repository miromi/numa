import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from avatar import Avatar

class TestAvatar(unittest.TestCase):
    """测试Avatar主类"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时配置文件
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        self.temp_config.write("""
backend:
  url: "http://localhost:7301"
  api_token: "test-token"

git:
  username: "testuser"
  email: "test@example.com"

avatar:
  id: "test_avatar"
  name: "Test Avatar"

llm:
  api_key: "test-api-key"
  model: "gpt-4"
  temperature: 0.7

polling:
  interval: 1
""")
        self.temp_config.close()
    
    def tearDown(self):
        """测试后清理"""
        os.unlink(self.temp_config.name)
    
    @patch('avatar.LLMService')
    @patch('avatar.GitService')
    @patch('avatar.CodeService')
    def test_avatar_initialization(self, mock_code_service, mock_git_service, mock_llm_service):
        """测试Avatar初始化"""
        # 创建Avatar实例
        avatar = Avatar(config_path=self.temp_config.name)
        
        # 验证组件是否正确初始化
        self.assertIsNotNone(avatar.config)
        self.assertIsNotNone(avatar.llm_service)
        self.assertIsNotNone(avatar.git_service)
        self.assertIsNotNone(avatar.code_service)
    
    @patch('avatar.LLMService')
    @patch('avatar.GitService')
    @patch('avatar.CodeService')
    @patch('avatar.CommandExecutor')
    def test_get_status(self, mock_executor, mock_code_service, mock_git_service, mock_llm_service):
        """测试获取Avatar状态"""
        # 创建Avatar实例
        avatar = Avatar(config_path=self.temp_config.name)
        
        # 获取状态
        status = avatar.get_status()
        
        # 验证状态信息
        self.assertIsInstance(status, dict)
        self.assertEqual(status["status"], "running")
        self.assertEqual(status["avatar_id"], "test_avatar")
        self.assertEqual(status["avatar_name"], "Test Avatar")
    
    @patch('avatar.LLMService')
    @patch('avatar.GitService')
    @patch('avatar.CodeService')
    @patch('avatar.CommandExecutor')
    def test_simulate_api_call(self, mock_executor, mock_code_service, mock_git_service, mock_llm_service):
        """测试模拟API调用"""
        # 创建Avatar实例
        avatar = Avatar(config_path=self.temp_config.name)
        
        # 调用模拟API方法
        task_data = avatar._simulate_api_call(123)
        
        # 验证返回的数据结构
        self.assertIsInstance(task_data, dict)
        self.assertEqual(task_data["id"], 123)
        self.assertIn("title", task_data)
        self.assertIn("description", task_data)
        self.assertIn("status", task_data)
        self.assertIn("code_branch", task_data)
        self.assertIn("application_id", task_data)
    
    @patch('avatar.LLMService')
    @patch('avatar.GitService')
    @patch('avatar.CodeService')
    @patch('avatar.CommandExecutor')
    def test_simulate_app_info(self, mock_executor, mock_code_service, mock_git_service, mock_llm_service):
        """测试模拟应用信息获取"""
        # 创建Avatar实例
        avatar = Avatar(config_path=self.temp_config.name)
        
        # 调用模拟API方法
        app_data = avatar._simulate_app_info(1)
        
        # 验证返回的数据结构
        self.assertIsInstance(app_data, dict)
        self.assertEqual(app_data["id"], 1)
        self.assertIn("name", app_data)
        self.assertIn("git_repo_url", app_data)

if __name__ == '__main__':
    unittest.main()