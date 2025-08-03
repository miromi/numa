import unittest
import os
import tempfile
from utils.executor import CommandExecutor

class TestCommandExecutor(unittest.TestCase):
    """测试命令执行工具"""
    
    def test_run_command_success(self):
        """测试成功执行命令"""
        # 执行一个简单的命令
        result = CommandExecutor.run_command(["echo", "test"])
        
        # 验证结果
        self.assertTrue(result["success"])
        self.assertEqual(result["returncode"], 0)
        self.assertIn("test", result["stdout"])
        self.assertEqual(result["stderr"], "")
    
    def test_run_command_failure(self):
        """测试执行失败的命令"""
        # 执行一个不存在的命令
        result = CommandExecutor.run_command(["nonexistent-command"])
        
        # 验证结果
        self.assertFalse(result["success"])
        self.assertNotEqual(result["returncode"], 0)
        self.assertIsInstance(result["stderr"], str)
    
    def test_run_command_with_cwd(self):
        """测试在指定目录执行命令"""
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            # 在临时目录创建一个文件
            test_file = os.path.join(temp_dir, "test.txt")
            with open(test_file, "w") as f:
                f.write("test content")
            
            # 在临时目录执行命令列出文件
            result = CommandExecutor.run_command(["ls"], cwd=temp_dir)
            
            # 验证结果
            self.assertTrue(result["success"])
            self.assertIn("test.txt", result["stdout"])
    
    def test_create_temp_dir(self):
        """测试创建临时目录"""
        # 创建临时目录
        temp_dir = CommandExecutor.create_temp_dir("test_prefix_")
        
        # 验证目录是否存在
        self.assertTrue(os.path.exists(temp_dir))
        self.assertTrue(os.path.isdir(temp_dir))
        self.assertIn("test_prefix_", temp_dir)
        
        # 清理
        CommandExecutor.remove_dir(temp_dir)
    
    def test_remove_dir(self):
        """测试删除目录"""
        # 创建临时目录
        temp_dir = CommandExecutor.create_temp_dir("test_remove_")
        
        # 确保目录存在
        self.assertTrue(os.path.exists(temp_dir))
        
        # 删除目录
        result = CommandExecutor.remove_dir(temp_dir)
        
        # 验证目录已被删除
        self.assertTrue(result)
        self.assertFalse(os.path.exists(temp_dir))
    
    def test_remove_nonexistent_dir(self):
        """测试删除不存在的目录"""
        # 尝试删除不存在的目录
        result = CommandExecutor.remove_dir("/nonexistent/directory")
        
        # 应该返回True（不会报错）
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()