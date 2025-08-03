import httpx
import json
from typing import Optional, Dict, Any, List
from utils.executor import CommandExecutor

class APIService:
    """API服务类，用于与后端通信"""
    
    def __init__(self, base_url: str, api_token: str = ""):
        self.base_url = base_url.rstrip('/')
        self.api_token = api_token
        self.headers = {
            "Content-Type": "application/json"
        }
        if api_token:
            self.headers["Authorization"] = f"Bearer {api_token}"
    
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
                elif method.lower() == "delete":
                    response = client.delete(url, headers=self.headers)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return None
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
            return None
        except Exception as e:
            print(f"Error making request to {url}: {e}")
            return None
    
    def get_task_topic(self, topic_name: str = "tasks") -> Optional[Dict[Any, Any]]:
        """获取任务消息topic
        
        Args:
            topic_name: topic名称，默认为"tasks"
            
        Returns:
            topic信息或None
        """
        # 如果是默认的"tasks" topic，使用专用接口
        if topic_name == "tasks":
            return self._make_request("get", "/api/topics/tasks")
        
        # 否则，通过名称搜索topic
        topics = self._make_request("get", "/api/topics")
        if topics and "data" in topics:
            for topic in topics["data"]:
                if topic.get("name") == topic_name:
                    return topic
        return None
    
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
    
    def update_task_status(self, task_id: int, status: str, details: Optional[Dict] = None) -> Optional[Dict[Any, Any]]:
        """更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            details: 状态详情
            
        Returns:
            更新结果或None
        """
        data = {"status": status}
        if details:
            data["details"] = details
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
    
    def health_check(self) -> bool:
        """检查后端服务健康状态
        
        Returns:
            是否健康
        """
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.base_url}/docs")
                return response.status_code == 200
        except:
            return False