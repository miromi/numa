import logging
import os
from datetime import datetime

class Logger:
    """日志工具类"""
    
    def __init__(self, name: str = "numa_avatar", log_file: str = "avatar.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 创建文件处理器
        if not any(isinstance(handler, logging.FileHandler) for handler in self.logger.handlers):
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.INFO)
            
            # 创建格式化器
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(formatter)
            
            # 添加处理器到日志器
            self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """记录信息日志"""
        self.logger.info(message)
    
    def error(self, message: str):
        """记录错误日志"""
        self.logger.error(message)
    
    def warning(self, message: str):
        """记录警告日志"""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """记录调试日志"""
        self.logger.debug(message)