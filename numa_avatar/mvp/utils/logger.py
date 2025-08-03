import logging
import os
from datetime import datetime
from typing import Optional

class Logger:
    """增强的日志服务类"""
    
    def __init__(self, name: str = "avatar", log_dir: str = "./logs", level: int = logging.INFO):
        self.name = name
        self.log_dir = log_dir
        self.level = level
        
        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            # 创建文件处理器
            log_file = os.path.join(log_dir, f"{name}.log")
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(level)
            
            # 创建控制台处理器
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            
            # 创建格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            
            # 添加处理器到logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)
    
    def debug(self, message: str):
        """记录debug级别日志"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """记录info级别日志"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """记录warning级别日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """记录error级别日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """记录critical级别日志"""
        self.logger.critical(message)
    
    def task_log(self, task_id: str, message: str, level: str = "info"):
        """记录任务特定日志"""
        task_log_file = os.path.join(self.log_dir, f"task_{task_id}.log")
        
        # 确保任务日志目录存在
        task_log_dir = os.path.join(self.log_dir, "tasks")
        if not os.path.exists(task_log_dir):
            os.makedirs(task_log_dir)
        
        task_log_file = os.path.join(task_log_dir, f"task_{task_id}.log")
        
        # 创建任务特定的logger
        task_logger = logging.getLogger(f"task_{task_id}")
        task_logger.setLevel(self.level)
        
        # 避免重复添加处理器
        if not task_logger.handlers:
            handler = logging.FileHandler(task_log_file, encoding='utf-8')
            handler.setLevel(self.level)
            formatter = logging.Formatter(
                '%(asctime)s - TASK-{task_id} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            task_logger.addHandler(handler)
        
        # 记录日志
        if level.lower() == "debug":
            task_logger.debug(message)
        elif level.lower() == "info":
            task_logger.info(message)
        elif level.lower() == "warning":
            task_logger.warning(message)
        elif level.lower() == "error":
            task_logger.error(message)
        elif level.lower() == "critical":
            task_logger.critical(message)
        else:
            task_logger.info(message)
    
    def get_log_file_path(self, task_id: Optional[str] = None) -> str:
        """获取日志文件路径"""
        if task_id:
            task_log_dir = os.path.join(self.log_dir, "tasks")
            if not os.path.exists(task_log_dir):
                os.makedirs(task_log_dir)
            return os.path.join(task_log_dir, f"task_{task_id}.log")
        else:
            return os.path.join(self.log_dir, f"{self.name}.log")