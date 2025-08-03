import unittest
import os
import tempfile
import shutil
from utils.logger import Logger

class TestLogger(unittest.TestCase):
    """测试日志服务"""
    
    def setUp(self):
        """测试前准备"""
        # 创建临时目录用于日志文件
        self.temp_dir = tempfile.mkdtemp(prefix="avatar_test_logs_")
    
    def tearDown(self):
        """测试后清理"""
        # 删除临时目录
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_logger_initialization(self):
        """测试日志服务初始化"""
        logger = Logger("test_logger", self.temp_dir)
        
        # 验证日志目录是否创建
        self.assertTrue(os.path.exists(self.temp_dir))
        
        # 验证主日志文件是否创建
        log_file = os.path.join(self.temp_dir, "test_logger.log")
        self.assertTrue(os.path.exists(log_file))
    
    def test_log_levels(self):
        """测试不同日志级别"""
        logger = Logger("test_levels", self.temp_dir)
        log_file = os.path.join(self.temp_dir, "test_levels.log")
        
        # 记录不同级别的日志
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")
        
        # 验证日志是否写入文件
        with open(log_file, 'r') as f:
            content = f.read()
            self.assertIn("Debug message", content)
            self.assertIn("Info message", content)
            self.assertIn("Warning message", content)
            self.assertIn("Error message", content)
            self.assertIn("Critical message", content)
    
    def test_task_log(self):
        """测试任务日志"""
        logger = Logger("test_task", self.temp_dir)
        
        # 记录任务日志
        logger.task_log("123", "Task started", "info")
        logger.task_log("123", "Task processing", "debug")
        logger.task_log("123", "Task completed", "info")
        
        # 验证任务日志文件是否存在
        task_log_dir = os.path.join(self.temp_dir, "tasks")
        task_log_file = os.path.join(task_log_dir, "task_123.log")
        self.assertTrue(os.path.exists(task_log_file))
        
        # 验证日志内容
        with open(task_log_file, 'r') as f:
            content = f.read()
            self.assertIn("Task started", content)
            self.assertIn("Task processing", content)
            self.assertIn("Task completed", content)
    
    def test_get_log_file_path(self):
        """测试获取日志文件路径"""
        logger = Logger("test_path", self.temp_dir)
        
        # 获取主日志文件路径
        main_log_path = logger.get_log_file_path()
        expected_main_path = os.path.join(self.temp_dir, "test_path.log")
        self.assertEqual(main_log_path, expected_main_path)
        
        # 获取任务日志文件路径
        task_log_path = logger.get_log_file_path("456")
        expected_task_path = os.path.join(self.temp_dir, "tasks", "task_456.log")
        self.assertEqual(task_log_path, expected_task_path)
        
        # 验证任务日志目录是否创建
        task_log_dir = os.path.join(self.temp_dir, "tasks")
        self.assertTrue(os.path.exists(task_log_dir))

if __name__ == '__main__':
    unittest.main()