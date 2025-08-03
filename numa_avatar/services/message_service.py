import time
import json
from typing import Optional, Dict, Any
from config import Config
from services.api_service import APIService
from utils.logger import Logger

class MessageService:
    """消息订阅服务类"""
    
    def __init__(self, config: Config, api_service: APIService):
        self.config = config
        self.api_service = api_service
        self.logger = Logger("message_service")
        self.polling_interval = config.get("polling.interval", 5)
        self.topic_id = None
    
    def subscribe_to_tasks(self) -> bool:
        """订阅任务消息
        
        Returns:
            是否成功订阅
        """
        topic_info = self.api_service.get_task_topic()
        if topic_info and "id" in topic_info:
            self.topic_id = topic_info["id"]
            self.logger.info(f"Successfully subscribed to task topic {self.topic_id}")
            return True
        else:
            self.logger.error("Failed to subscribe to task topic")
            return False
    
    def poll_messages(self) -> Optional[Dict[Any, Any]]:
        """轮询消息
        
        Returns:
            消息数据或None
        """
        if not self.topic_id:
            self.logger.warning("Not subscribed to any topic")
            return None
        
        messages = self.api_service.get_messages(self.topic_id)
        return messages
    
    def start_polling(self, callback):
        """开始轮询消息
        
        Args:
            callback: 处理消息的回调函数
        """
        if not self.topic_id:
            self.logger.error("Not subscribed to any topic, cannot start polling")
            return
        
        self.logger.info("Starting message polling...")
        while True:
            try:
                messages = self.poll_messages()
                if messages and "data" in messages:
                    for message in messages["data"]:
                        callback(message)
                time.sleep(self.polling_interval)
            except KeyboardInterrupt:
                self.logger.info("Polling interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"Error during polling: {e}")
                time.sleep(self.polling_interval)