import unittest
import os
import tempfile
from unittest.mock import patch, MagicMock
from services.code_service import CodeService
from llm.llm_service import LLMService

class TestCodeService(unittest.TestCase):
    """测试代码服务"""
    
    def setUp(self):
        """测试前准备"""
        # 创建模拟的LLM服务
        self.mock_llm_service = MagicMock()
        self.code_service = CodeService(self.mock_llm_service)
    
    def test_parse_generated_code(self):
        """测试代码解析功能"""
        # 准备测试数据
        generated_code = """
FILE: src/login.js
CONTENT:
console.log('Login feature');
function login() {
  // Login implementation
}
END_FILE

FILE: src/utils.js
CONTENT:
export function validateEmail(email) {
  return email.includes('@');
}
END_FILE
        """
        
        # 执行测试
        files = self.code_service._parse_generated_code(generated_code)
        
        # 验证结果
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0][0], "src/login.js")
        self.assertIn("console.log('Login feature');", files[0][1])
        self.assertEqual(files[1][0], "src/utils.js")
        self.assertIn("validateEmail", files[1][1])
    
    def test_write_files(self):
        """测试文件写入功能"""
        # 准备测试数据
        files = [
            ("test_dir/test_file1.txt", "Content of file 1"),
            ("test_dir/subdir/test_file2.txt", "Content of file 2")
        ]
        
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 执行测试
            self.code_service.write_files(files, temp_dir)
            
            # 验证文件是否正确创建
            file1_path = os.path.join(temp_dir, "test_dir/test_file1.txt")
            file2_path = os.path.join(temp_dir, "test_dir/subdir/test_file2.txt")
            
            self.assertTrue(os.path.exists(file1_path))
            self.assertTrue(os.path.exists(file2_path))
            
            with open(file1_path, 'r') as f:
                self.assertEqual(f.read(), "Content of file 1")
            
            with open(file2_path, 'r') as f:
                self.assertEqual(f.read(), "Content of file 2")
    
    @patch('services.code_service.LLMService')
    def test_analyze_task(self, mock_llm_class):
        """测试任务分析功能"""
        # 设置模拟LLM服务返回值
        mock_llm_instance = MagicMock()
        mock_llm_instance.analyze_task.return_value = {
            "functional_requirements": ["用户登录"],
            "technical_requirements": ["JWT验证"],
            "files_to_create": ["/src/login.js"],
            "files_to_modify": [],
            "estimated_complexity": "简单"
        }
        mock_llm_class.return_value = mock_llm_instance
        
        # 创建CodeService实例
        code_service = CodeService(mock_llm_instance)
        
        # 执行测试
        result = code_service.analyze_task("实现用户登录功能")
        
        # 验证结果
        self.assertIsInstance(result, dict)
        self.assertIn("functional_requirements", result)
        self.assertIn("technical_requirements", result)

if __name__ == '__main__':
    unittest.main()