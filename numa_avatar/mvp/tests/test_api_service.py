import unittest
from unittest.mock import patch, MagicMock
from services.api_service import APIService

class TestAPIService(unittest.TestCase):
    """测试API服务"""
    
    def setUp(self):
        """测试前准备"""
        self.base_url = "http://localhost:7301"
        self.api_token = "test-token"
        self.api_service = APIService(self.base_url, self.api_token)
    
    @patch('services.api_service.httpx.Client')
    def test_get_task_topic(self, mock_client):
        """测试获取任务topic"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "tasks"}
        mock_response.raise_for_status.return_value = None
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        
        # 执行测试
        result = self.api_service.get_task_topic()
        
        # 验证结果
        self.assertEqual(result, {"id": 1, "name": "tasks"})
        mock_client.return_value.__enter__.return_value.get.assert_called_once_with(
            f"{self.base_url}/api/topics/tasks",
            headers=self.api_service.headers
        )
    
    @patch('services.api_service.httpx.Client')
    def test_get_messages(self, mock_client):
        """测试获取消息"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": 1, "data": {"task_id": 123}}]}
        mock_response.raise_for_status.return_value = None
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        
        # 执行测试
        result = self.api_service.get_messages(1)
        
        # 验证结果
        self.assertEqual(result, {"data": [{"id": 1, "data": {"task_id": 123}}]})
        mock_client.return_value.__enter__.return_value.get.assert_called_once_with(
            f"{self.base_url}/api/topics/1/messages",
            headers=self.api_service.headers
        )
    
    @patch('services.api_service.httpx.Client')
    def test_get_task(self, mock_client):
        """测试获取任务详情"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123, "title": "Test Task"}
        mock_response.raise_for_status.return_value = None
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        
        # 执行测试
        result = self.api_service.get_task(123)
        
        # 验证结果
        self.assertEqual(result, {"id": 123, "title": "Test Task"})
        mock_client.return_value.__enter__.return_value.get.assert_called_once_with(
            f"{self.base_url}/api/tasks/123",
            headers=self.api_service.headers
        )
    
    @patch('services.api_service.httpx.Client')
    def test_update_task_status(self, mock_client):
        """测试更新任务状态"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 123, "status": "done"}
        mock_response.raise_for_status.return_value = None
        mock_client.return_value.__enter__.return_value.put.return_value = mock_response
        
        # 执行测试
        result = self.api_service.update_task_status(123, "done")
        
        # 验证结果
        self.assertEqual(result, {"id": 123, "status": "done"})
        mock_client.return_value.__enter__.return_value.put.assert_called_once_with(
            f"{self.base_url}/api/tasks/123/status",
            headers=self.api_service.headers,
            json={"status": "done"}
        )
    
    @patch('services.api_service.httpx.Client')
    def test_post_task_logs(self, mock_client):
        """测试上报任务日志"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None
        mock_client.return_value.__enter__.return_value.post.return_value = mock_response
        
        # 执行测试
        result = self.api_service.post_task_logs(123, "Test log message")
        
        # 验证结果
        self.assertEqual(result, {"success": True})
        mock_client.return_value.__enter__.return_value.post.assert_called_once_with(
            f"{self.base_url}/api/tasks/123/logs",
            headers=self.api_service.headers,
            json={"logs": "Test log message"}
        )
    
    @patch('services.api_service.httpx.Client')
    def test_get_application(self, mock_client):
        """测试获取应用信息"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": 1, "name": "Test App"}
        mock_response.raise_for_status.return_value = None
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        
        # 执行测试
        result = self.api_service.get_application(1)
        
        # 验证结果
        self.assertEqual(result, {"id": 1, "name": "Test App"})
        mock_client.return_value.__enter__.return_value.get.assert_called_once_with(
            f"{self.base_url}/api/applications/1",
            headers=self.api_service.headers
        )
    
    @patch('services.api_service.httpx.Client')
    def test_health_check_success(self, mock_client):
        """测试健康检查成功"""
        # 设置模拟响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_client.return_value.__enter__.return_value.get.return_value = mock_response
        
        # 执行测试
        result = self.api_service.health_check()
        
        # 验证结果
        self.assertTrue(result)
        mock_client.return_value.__enter__.return_value.get.assert_called_once_with(
            f"{self.base_url}/docs"
        )
    
    @patch('services.api_service.httpx.Client')
    def test_health_check_failure(self, mock_client):
        """测试健康检查失败"""
        # 设置模拟异常
        mock_client.return_value.__enter__.return_value.get.side_effect = Exception("Connection failed")
        
        # 执行测试
        result = self.api_service.health_check()
        
        # 验证结果
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()