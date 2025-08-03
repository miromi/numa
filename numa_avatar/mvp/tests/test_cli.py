import unittest
import os
import sys
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, project_root)

from cli.qwen import load_config, get_api_key, process_requirement


class TestCLI(unittest.TestCase):
    """测试CLI工具"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录用于测试
        self.temp_dir = tempfile.mkdtemp(prefix="qwen_cli_test_")
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_config_no_file(self):
        """测试加载不存在的配置文件"""
        # 临时更改工作目录
        original_cwd = os.getcwd()
        os.chdir(self.temp_dir)
        
        try:
            # 调用函数
            config = load_config()
            
            # 验证结果
            self.assertIsInstance(config, dict)
            self.assertEqual(config, {})
        finally:
            # 恢复工作目录
            os.chdir(original_cwd)
    
    @patch('cli.qwen.os.environ.get')
    def test_get_api_key_from_env(self, mock_environ_get):
        """测试从环境变量获取API密钥"""
        # 设置模拟环境变量
        mock_environ_get.return_value = "test-api-key-from-env"
        
        # 调用函数
        api_key = get_api_key()
        
        # 验证结果
        self.assertEqual(api_key, "test-api-key-from-env")
        mock_environ_get.assert_called_once_with("OPENAI_API_KEY")
    
    @patch('cli.qwen.os.environ.get')
    @patch('cli.qwen.load_config')
    def test_get_api_key_from_config(self, mock_load_config, mock_environ_get):
        """测试从配置文件获取API密钥"""
        # 设置模拟环境变量返回None
        mock_environ_get.return_value = None
        
        # 设置模拟配置文件
        mock_load_config.return_value = {
            "llm": {
                "api_key": "test-api-key-from-config"
            }
        }
        
        # 调用函数
        api_key = get_api_key()
        
        # 验证结果
        self.assertEqual(api_key, "test-api-key-from-config")
        mock_environ_get.assert_called_once_with("OPENAI_API_KEY")
        mock_load_config.assert_called_once()
    
    @patch('cli.qwen.get_api_key')
    @patch('cli.qwen.LLMService')
    @patch('cli.qwen.CodeService')
    def test_process_requirement_success(self, mock_code_service_class, mock_llm_service_class, mock_get_api_key):
        """测试成功处理需求"""
        # 设置模拟返回值
        mock_get_api_key.return_value = "test-api-key"
        
        # 创建模拟服务实例
        mock_llm_service = MagicMock()
        mock_code_service = MagicMock()
        
        mock_llm_service_class.return_value = mock_llm_service
        mock_code_service_class.return_value = mock_code_service
        
        # 设置模拟方法返回值
        mock_code_service.analyze_task.return_value = {
            "functional_requirements": ["功能1"],
            "technical_requirements": ["技术1"]
        }
        mock_code_service.generate_code_files.return_value = [
            ("test.py", "print('Hello')")
        ]
        
        # 调用函数
        result = process_requirement("测试需求", self.temp_dir)
        
        # 验证结果
        self.assertTrue(result)
        mock_get_api_key.assert_called_once()
        mock_llm_service_class.assert_called_once_with("test-api-key", "gpt-4", 0.7)
        mock_code_service_class.assert_called_once_with(mock_llm_service)
        mock_code_service.analyze_task.assert_called_once_with("测试需求")
        mock_code_service.generate_code_files.assert_called_once_with("测试需求")
        mock_code_service.write_files.assert_called_once()
    
    @patch('cli.qwen.get_api_key')
    def test_process_requirement_no_api_key(self, mock_get_api_key):
        """测试没有API密钥时处理需求"""
        # 设置模拟返回值
        mock_get_api_key.return_value = ""
        
        # 调用函数
        result = process_requirement("测试需求", self.temp_dir)
        
        # 验证结果
        self.assertFalse(result)
        mock_get_api_key.assert_called_once()


if __name__ == '__main__':
    unittest.main()