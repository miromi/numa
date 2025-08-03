from config import Config
from services.api_service import APIService
from services.message_service import MessageService
from services.git_service import GitService
from services.task_service import TaskService
from utils.logger import Logger

class Avatar:
    """Avatar主类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = Config(config_path)
        self.logger = Logger("avatar")
        self.api_service = APIService(self.config)
        self.git_service = GitService(
            username=self.config.get("git.username", ""),
            email=self.config.get("git.email", "")
        )
        self.message_service = MessageService(self.config, self.api_service)
        self.task_service = TaskService(self.config, self.api_service, self.git_service)
        
        self.logger.info("Avatar initialized")
    
    def _handle_message(self, message):
        """处理接收到的消息
        
        Args:
            message: 消息数据
        """
        self.logger.info(f"Received message: {message}")
        
        # 解析消息，获取任务ID
        if "data" in message and "task_id" in message["data"]:
            task_id = message["data"]["task_id"]
            self.logger.info(f"Processing task {task_id}")
            
            # 执行任务
            success = self.task_service.execute_task(task_id)
            if success:
                self.logger.info(f"Task {task_id} completed successfully")
            else:
                self.logger.error(f"Task {task_id} failed")
        else:
            self.logger.warning("Received message without task_id")
    
    def start(self):
        """启动Avatar"""
        self.logger.info("Starting Avatar...")
        
        # 订阅任务消息
        if not self.message_service.subscribe_to_tasks():
            self.logger.error("Failed to subscribe to tasks")
            return
        
        # 开始轮询消息
        self.message_service.start_polling(self._handle_message)
    
    def get_status(self):
        """获取Avatar状态"""
        return {
            "status": "running",
            "avatar_id": self.config.get("avatar.id"),
            "avatar_name": self.config.get("avatar.name")
        }