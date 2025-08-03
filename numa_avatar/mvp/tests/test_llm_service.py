import unittest
import os
from unittest.mock import patch, MagicMock
from llm.llm_service import LLMService

class TestLLMService(unittest.TestCase):
    """测试LLM服务"""
    
    def setUp(self):
        """测试前准备"""
        api_key = os.environ.get("OPENAI_API_KEY", "test-key")
        self.llm_service = LLMService(api_key=api_key, model="gpt-4", temperature=0.7)
    
    @patch('llm.llm_service.OpenAI')
    def test_analyze_task(self, mock_openai):
        """测试任务分析功能"""
        # 模拟OpenAI客户端响应
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"functional_requirements": ["用户登录"], "technical_requirements": ["JWT验证"], "files_to_create": ["/src/login.js"], "files_to_modify": [], "estimated_complexity": "简单"}'
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # 执行测试
        result = self.llm_service.analyze_task("实现用户登录功能")
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertIn("functional_requirements", result)
        self.assertIn("technical_requirements", result)
        self.assertIn("files_to_create", result)
        self.assertIn("files_to_modify", result)
        self.assertIn("estimated_complexity", result)
    
    @patch('llm.llm_service.OpenAI')
    def test_generate_code(self, mock_openai):
        """测试代码生成功能"""
        # 模拟OpenAI客户端响应
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "FILE: src/login.js\nCONTENT:\nconsole.log('Login feature');\nEND_FILE"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # 执行测试
        result = self.llm_service.generate_code("实现用户登录功能")
        
        # 验证结果包含关键标识
        self.assertIn("FILE:", result)
        self.assertIn("CONTENT:", result)
        self.assertIn("END_FILE", result)
    
    @patch('llm.llm_service.OpenAI')
    def test_fix_code(self, mock_openai):
        """测试代码修复功能"""
        # 模拟OpenAI客户端响应
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "console.log('Fixed code');"
        mock_openai.return_value.chat.completions.create.return_value = mock_response
        
        # 执行测试
        result = self.llm_service.fix_code("SyntaxError: Unexpected token", "console.log('Broken code')")
        
        # 验证结果
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)

if __name__ == '__main__':
    unittest.main()