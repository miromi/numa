import time
import json
from typing import Optional, Callable, Dict, Any
from services.api_service import APIService

class MessageService:
    """消息订阅服务类"""
    
    def __init__(self, api_service: APIService, polling_interval: int = 5, topic_name: str = "tasks"):
        self.api_service = api_service
        self.polling_interval = polling_interval
        self.topic_name = topic_name
        self.topic_id = None
        self.subscribed = False
    
    def subscribe_to_tasks(self) -> bool:
        """订阅任务消息
        
        Returns:
            是否成功订阅
        """
        topic_info = self.api_service.get_task_topic(self.topic_name)
        if topic_info and "id" in topic_info:
            self.topic_id = topic_info["id"]
            self.subscribed = True
            print(f"Successfully subscribed to task topic '{self.topic_name}' (ID: {self.topic_id})")
            return True
        else:
            print(f"Failed to subscribe to task topic '{self.topic_name}'")
            return False
    
    def poll_messages(self) -> Optional[Dict[Any, Any]]:
        """轮询消息
        
        Returns:
            消息数据或None
        """
        if not self.subscribed or not self.topic_id:
            print("Not subscribed to any topic")
            return None
        
        messages = self.api_service.get_messages(self.topic_id)
        return messages
    
    def start_polling(self, callback: Callable[[Dict], None]):
        """开始轮询消息
        
        Args:
            callback: 处理消息的回调函数
        """
        if not self.subscribed or not self.topic_id:
            print("Not subscribed to any topic, cannot start polling")
            return
        
        print(f"Starting message polling for topic '{self.topic_name}'...")
        while True:
            try:
                messages = self.poll_messages()
                if messages and "data" in messages:
                    for message in messages["data"]:
                        callback(message)
                time.sleep(self.polling_interval)
            except KeyboardInterrupt:
                print("Polling interrupted by user")
                break
            except Exception as e:
                print(f"Error during polling: {e}")
                time.sleep(self.polling_interval)