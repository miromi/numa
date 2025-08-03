import httpx
from typing import Optional, Dict, Any
from config import Config
from utils.logger import Logger

class APIService:
    """API服务类，用于与后端通信"""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = Logger("api_service")
        self.base_url = config.get("backend.url", "http://localhost:7301")
        self.api_token = config.get("backend.api_token", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[Any, Any]] = None) -> Optional[Dict[Any, Any]]:
        """发送HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求数据
            
        Returns:
            响应数据或None
        """
        url = f"{self.base_url}{endpoint}"
        try:
            with httpx.Client() as client:
                if method.lower() == "get":
                    response = client.get(url, headers=self.headers)
                elif method.lower() == "post":
                    response = client.post(url, headers=self.headers, json=data)
                elif method.lower() == "put":
                    response = client.put(url, headers=self.headers, json=data)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            self.logger.error(f"HTTP error occurred: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error making request to {url}: {e}")
            return None
    
    def get_task_topic(self) -> Optional[Dict[Any, Any]]:
        """获取任务消息topic
        
        Returns:
            topic信息或None
        """
        return self._make_request("get", "/api/topics/tasks")
    
    def get_messages(self, topic_id: int) -> Optional[Dict[Any, Any]]:
        """从topic获取消息
        
        Args:
            topic_id: topic ID
            
        Returns:
            消息列表或None
        """
        return self._make_request("get", f"/api/topics/{topic_id}/messages")
    
    def get_task(self, task_id: int) -> Optional[Dict[Any, Any]]:
        """获取任务详情
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务详情或None
        """
        return self._make_request("get", f"/api/tasks/{task_id}")
    
    def update_task_status(self, task_id: int, status: str) -> Optional[Dict[Any, Any]]:
        """更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            
        Returns:
            更新结果或None
        """
        data = {"status": status}
        return self._make_request("put", f"/api/tasks/{task_id}/status", data)
    
    def post_task_logs(self, task_id: int, logs: str) -> Optional[Dict[Any, Any]]:
        """上报任务执行日志
        
        Args:
            task_id: 任务ID
            logs: 日志内容
            
        Returns:
            上报结果或None
        """
        data = {"logs": logs}
        return self._make_request("post", f"/api/tasks/{task_id}/logs", data)
    
    def get_application(self, app_id: int) -> Optional[Dict[Any, Any]]:
        """获取应用信息
        
        Args:
            app_id: 应用ID
            
        Returns:
            应用信息或None
        """
        return self._make_request("get", f"/api/applications/{app_id}")