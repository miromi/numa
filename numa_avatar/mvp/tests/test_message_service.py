import unittest
from unittest.mock import patch, MagicMock, call
from services.message_service import MessageService
from services.api_service import APIService

class TestMessageService(unittest.TestCase):
    """测试消息服务"""
    
    def setUp(self):
        """测试前准备"""
        self.api_service = MagicMock()
        self.message_service = MessageService(self.api_service, polling_interval=1)
    
    def test_subscribe_to_tasks_success(self):
        """测试成功订阅任务"""
        # 设置模拟API服务返回值
        self.api_service.get_task_topic.return_value = {"id": 1, "name": "tasks"}
        
        # 执行测试
        result = self.message_service.subscribe_to_tasks()
        
        # 验证结果
        self.assertTrue(result)
        self.assertEqual(self.message_service.topic_id, 1)
        self.assertTrue(self.message_service.subscribed)
        self.api_service.get_task_topic.assert_called_once()
    
    def test_subscribe_to_tasks_failure(self):
        """测试订阅任务失败"""
        # 设置模拟API服务返回值
        self.api_service.get_task_topic.return_value = None
        
        # 执行测试
        result = self.message_service.subscribe_to_tasks()
        
        # 验证结果
        self.assertFalse(result)
        self.assertIsNone(self.message_service.topic_id)
        self.assertFalse(self.message_service.subscribed)
    
    def test_poll_messages_success(self):
        """测试成功轮询消息"""
        # 设置消息服务状态
        self.message_service.subscribed = True
        self.message_service.topic_id = 1
        
        # 设置模拟API服务返回值
        mock_messages = {"data": [{"id": 1, "data": {"task_id": 123}}]}
        self.api_service.get_messages.return_value = mock_messages
        
        # 执行测试
        result = self.message_service.poll_messages()
        
        # 验证结果
        self.assertEqual(result, mock_messages)
        self.api_service.get_messages.assert_called_once_with(1)
    
    def test_poll_messages_not_subscribed(self):
        """测试未订阅时轮询消息"""
        # 设置消息服务状态
        self.message_service.subscribed = False
        
        # 执行测试
        result = self.message_service.poll_messages()
        
        # 验证结果
        self.assertIsNone(result)
    
    def test_poll_messages_no_topic(self):
        """测试没有topic时轮询消息"""
        # 设置消息服务状态
        self.message_service.subscribed = True
        self.message_service.topic_id = None
        
        # 执行测试
        result = self.message_service.poll_messages()
        
        # 验证结果
        self.assertIsNone(result)
    
    @patch('services.message_service.time.sleep')
    def test_start_polling_success(self, mock_sleep):
        """测试成功开始轮询"""
        # 设置消息服务状态
        self.message_service.subscribed = True
        self.message_service.topic_id = 1
        
        # 设置模拟API服务返回值
        self.api_service.get_messages.return_value = {
            "data": [
                {"id": 1, "data": {"task_id": 123}},
                {"id": 2, "data": {"task_id": 456}}
            ]
        }
        
        # 创建回调函数
        callback = MagicMock()
        
        # 为了防止无限循环，我们需要模拟time.sleep来抛出KeyboardInterrupt
        mock_sleep.side_effect = KeyboardInterrupt()
        
        # 执行测试
        self.message_service.start_polling(callback)
        
        # 验证结果
        self.api_service.get_messages.assert_called_with(1)
        # 验证回调函数被调用了两次
        callback.assert_has_calls([
            call({"id": 1, "data": {"task_id": 123}}),
            call({"id": 2, "data": {"task_id": 456}})
        ])
    
    def test_start_polling_not_subscribed(self):
        """测试未订阅时开始轮询"""
        # 设置消息服务状态
        self.message_service.subscribed = False
        
        # 创建回调函数
        callback = MagicMock()
        
        # 执行测试
        self.message_service.start_polling(callback)
        
        # 验证回调函数没有被调用
        callback.assert_not_called()

if __name__ == '__main__':
    unittest.main()