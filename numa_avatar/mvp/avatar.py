import os
import time
import json
from typing import Optional, Dict, Any
from config import Config
from llm.llm_service import LLMService
from services.git_service import GitService
from services.code_service import CodeService
from services.api_service import APIService
from services.message_service import MessageService
from utils.executor import CommandExecutor
from utils.logger import Logger
from workspace import WorkspaceManager

class Avatar:
    """Avatar主类（MVP版本）"""
    
    def __init__(self, config_path: str = "config.yaml"):
        # 如果存在本地配置文件，则优先使用
        if os.path.exists("config.local.yaml"):
            config_path = "config.local.yaml"
        self.config = Config(config_path)
        self.llm_service = LLMService(
            api_key=self.config.get("llm.api_key"),
            model=self.config.get("llm.model", "gpt-4"),
            temperature=self.config.get("llm.temperature", 0.7)
        )
        self.git_service = GitService(
            username=self.config.get("git.username", ""),
            email=self.config.get("git.email", "")
        )
        self.code_service = CodeService(self.llm_service)
        
        # 初始化日志服务
        log_dir = self.config.get("avatar.log_dir", "./logs")
        self.logger = Logger("avatar", log_dir)
        
        # 初始化API服务
        backend_url = self.config.get("backend.url", "http://localhost:7301")
        api_token = self.config.get("backend.api_token", "")
        self.api_service = APIService(backend_url, api_token)
        
        # 初始化消息服务
        polling_interval = self.config.get("polling.interval", 5)
        topic_name = self.config.get("avatar.topic_name", "tasks")
        self.message_service = MessageService(self.api_service, polling_interval, topic_name)
        
        # 初始化工作区
        workspace_path = self.config.get("avatar.workspace", "./workspace")
        self.workspace = WorkspaceManager(workspace_path)
        
        self.logger.info("Avatar MVP initialized")
        self.logger.info(f"Backend URL: {backend_url}")
        self.logger.info(f"Workspace: {workspace_path}")
        self.logger.info(f"Topic name: {topic_name}")
    
    def get_task(self, task_id: int) -> Optional[Dict[str, Any]]:
        """获取任务详情
        
        Args:
            task_id: 任务ID
            
        Returns:
            任务详情或None
        """
        self.logger.info(f"Getting task {task_id}")
        return self.api_service.get_task(task_id)
    
    def get_application(self, app_id: int) -> Optional[Dict[str, Any]]:
        """获取应用信息
        
        Args:
            app_id: 应用ID
            
        Returns:
            应用信息或None
        """
        self.logger.info(f"Getting application {app_id}")
        return self.api_service.get_application(app_id)
    
    def update_task_status(self, task_id: int, status: str, details: Optional[Dict] = None) -> bool:
        """更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            details: 状态详情
            
        Returns:
            是否成功更新
        """
        self.logger.info(f"Updating task {task_id} status to {status}")
        if details:
            self.logger.debug(f"Status details: {details}")
        
        result = self.api_service.update_task_status(task_id, status, details)
        return result is not None
    
    def post_task_logs(self, task_id: int, logs: str) -> bool:
        """上报任务执行日志
        
        Args:
            task_id: 任务ID
            logs: 日志内容
            
        Returns:
            是否成功上报
        """
        self.logger.info(f"Posting logs for task {task_id}")
        self.logger.debug(f"Logs content: {logs}")
        
        result = self.api_service.post_task_logs(task_id, logs)
        return result is not None
    
    def execute_task(self, task_id: int) -> bool:
        """执行任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功执行
        """
        self.logger.info(f"Starting execution of task {task_id}")
        
        # 记录任务开始时间
        start_time = time.time()
        
        try:
            # 1. 获取任务详情
            task_data = self.get_task(task_id)
            if not task_data:
                self.logger.error(f"Failed to get task {task_id}")
                self.update_task_status(task_id, "failed", {"error": "Failed to get task info"})
                return False
            
            self.logger.info(f"Task: {task_data['title']}")
            self.logger.info(f"Description: {task_data['description']}")
            
            # 更新任务状态为进行中
            self.update_task_status(task_id, "in_progress", {"step": "getting_task_info"})
            
            # 2. 获取应用信息
            app_data = self.get_application(task_data["application_id"])
            if not app_data:
                self.logger.error(f"Failed to get application {task_data['application_id']}")
                self.update_task_status(task_id, "failed", {"error": "Failed to get application info"})
                return False
            
            self.logger.info(f"Application: {app_data['name']}")
            
            # 更新任务状态
            self.update_task_status(task_id, "in_progress", {"step": "getting_application_info"})
            
            # 3. 克隆代码仓库到工作区
            repo_path = self.workspace.get_repo_path(f"app_{task_data['application_id']}")
            self.logger.info(f"Repository path: {repo_path}")
            
            if not os.path.exists(repo_path):
                self.logger.info("Cloning repository")
                self.update_task_status(task_id, "in_progress", {"step": "cloning_repository"})
                
                if not self.git_service.clone_repository(app_data["git_repo_url"], repo_path):
                    self.logger.error("Failed to clone repository")
                    self.update_task_status(task_id, "failed", {"error": "Failed to clone repository"})
                    return False
            else:
                self.logger.info(f"Repository already exists at {repo_path}")
            
            # 更新任务状态
            self.update_task_status(task_id, "in_progress", {"step": "repository_ready"})
            
            # 4. 切换到开发分支
            self.logger.info(f"Checking out branch {task_data['code_branch']}")
            self.update_task_status(task_id, "in_progress", {"step": "checking_out_branch"})
            
            if not self.git_service.checkout_branch(repo_path, task_data["code_branch"]):
                self.logger.error("Failed to checkout branch")
                self.update_task_status(task_id, "failed", {"error": "Failed to checkout branch"})
                return False
            
            # 更新任务状态
            self.update_task_status(task_id, "in_progress", {"step": "branch_checked_out"})
            
            # 5. 分析任务
            self.logger.info("Analyzing task")
            self.update_task_status(task_id, "in_progress", {"step": "analyzing_task"})
            
            task_analysis = self.code_service.analyze_task(task_data["description"])
            self.logger.info(f"Task analysis: {task_analysis}")
            
            # 上报任务分析日志
            self.post_task_logs(task_id, f"Task analysis: {json.dumps(task_analysis, ensure_ascii=False)}")
            
            # 更新任务状态
            self.update_task_status(task_id, "in_progress", {"step": "task_analyzed"})
            
            # 6. 生成代码
            self.logger.info("Generating code")
            self.update_task_status(task_id, "in_progress", {"step": "generating_code"})
            
            files = self.code_service.generate_code_files(
                task_data["description"], 
                f"这是一个{app_data['name']}应用程序"
            )
            
            if not files:
                self.logger.warning("No files generated")
                self.update_task_status(task_id, "failed", {"error": "No files generated"})
                return False
            
            self.logger.info(f"Generated {len(files)} files")
            
            # 上报代码生成日志
            self.post_task_logs(task_id, f"Generated {len(files)} files")
            
            # 更新任务状态
            self.update_task_status(task_id, "in_progress", {"step": "code_generated"})
            
            # 7. 写入文件到仓库
            self.logger.info("Writing files")
            self.update_task_status(task_id, "in_progress", {"step": "writing_files"})
            
            self.code_service.write_files(files, repo_path)
            
            # 更新任务状态
            self.update_task_status(task_id, "in_progress", {"step": "files_written"})
            
            # 8. 运行测试（简化处理）
            self.logger.info("Running tests")
            self.update_task_status(task_id, "in_progress", {"step": "running_tests"})
            
            # 在实际实现中，这里会运行项目测试
            self.post_task_logs(task_id, "Running tests...")
            
            # 更新任务状态
            self.update_task_status(task_id, "in_progress", {"step": "tests_completed"})
            
            # 9. 提交代码
            self.logger.info("Committing changes")
            self.update_task_status(task_id, "in_progress", {"step": "committing_changes"})
            
            commit_message = f"feat: Complete development task {task_id} - {task_data['title']}"
            if not self.git_service.commit_changes(repo_path, commit_message):
                self.logger.error("Failed to commit changes")
                self.update_task_status(task_id, "failed", {"error": "Failed to commit changes"})
                return False
            
            self.logger.info("Pushing changes")
            self.update_task_status(task_id, "in_progress", {"step": "pushing_changes"})
            
            if not self.git_service.push_changes(repo_path, task_data["code_branch"]):
                self.logger.error("Failed to push changes")
                self.update_task_status(task_id, "failed", {"error": "Failed to push changes"})
                return False
            
            # 记录任务完成时间
            end_time = time.time()
            duration = end_time - start_time
            
            # 更新任务状态为完成
            self.update_task_status(task_id, "done", {"duration": duration})
            self.logger.info(f"Task {task_id} executed successfully in {duration:.2f} seconds")
            
            # 记录任务到任务日志
            self.logger.task_log(str(task_id), f"Task completed successfully in {duration:.2f} seconds")
            
            return True
        except Exception as e:
            # 记录异常信息
            self.logger.error(f"Error executing task {task_id}: {e}")
            
            # 更新任务状态为失败
            end_time = time.time()
            duration = end_time - start_time
            self.update_task_status(task_id, "failed", {
                "error": str(e),
                "duration": duration
            })
            
            # 记录任务到任务日志
            self.logger.task_log(str(task_id), f"Task failed after {duration:.2f} seconds: {str(e)}", "error")
            
            return False
        finally:
            # 清理任务临时目录
            self.logger.info(f"Cleaning up temporary files for task {task_id}")
            self.workspace.cleanup_temp(str(task_id))
    
    def _handle_message(self, message: Dict):
        """处理接收到的消息
        
        Args:
            message: 消息数据
        """
        self.logger.info(f"Received message: {message}")
        
        # 解析消息，获取任务ID
        if "data" in message and "task_id" in message["data"]:
            task_id = message["data"]["task_id"]
            self.logger.info(f"Processing task {task_id}")
            
            # 记录任务到任务日志
            self.logger.task_log(str(task_id), f"Starting task processing")
            
            # 执行任务
            success = self.execute_task(task_id)
            if success:
                self.logger.info(f"Task {task_id} completed successfully")
                self.logger.task_log(str(task_id), "Task completed successfully")
            else:
                self.logger.error(f"Task {task_id} failed")
                self.logger.task_log(str(task_id), "Task failed", "error")
        else:
            self.logger.warning("Received message without task_id")
    
    def start(self):
        """启动Avatar"""
        self.logger.info("Starting Avatar...")
        
        # 检查后端服务是否可用
        if not self.api_service.health_check():
            self.logger.error("Backend service is not available. Please check the connection.")
            return
        
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
            "avatar_name": self.config.get("avatar.name"),
            "workspace": self.config.get("avatar.workspace", "./workspace"),
            "backend_url": self.config.get("backend.url", "http://localhost:7301"),
            "topic_name": self.config.get("avatar.topic_name", "tasks"),
            "log_dir": self.config.get("avatar.log_dir", "./logs")
        }