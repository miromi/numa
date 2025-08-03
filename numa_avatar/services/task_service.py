from typing import Optional
from config import Config
from models.task import Task
from models.application import Application
from services.api_service import APIService
from services.git_service import GitService
from utils.executor import CommandExecutor
from utils.logger import Logger

class TaskService:
    """任务执行服务类"""
    
    def __init__(self, config: Config, api_service: APIService, git_service: GitService):
        self.config = config
        self.api_service = api_service
        self.git_service = git_service
        self.logger = Logger("task_service")
    
    def execute_task(self, task_id: int) -> bool:
        """执行任务
        
        Args:
            task_id: 任务ID
            
        Returns:
            是否成功执行
        """
        self.logger.info(f"Starting execution of task {task_id}")
        
        # 1. 获取任务详情
        task_data = self.api_service.get_task(task_id)
        if not task_data:
            self.logger.error(f"Failed to get task {task_id}")
            return False
        
        task = Task(**task_data)
        
        # 2. 获取应用信息
        app_data = self.api_service.get_application(task.application_id)
        if not app_data:
            self.logger.error(f"Failed to get application {task.application_id}")
            return False
        
        application = Application(**app_data)
        
        # 3. 克隆代码仓库
        local_path = CommandExecutor.create_temp_dir(f"numa_repo_{task.application_id}_")
        if not self.git_service.clone_repository(application.git_repo_url, local_path):
            self.logger.error("Failed to clone repository")
            CommandExecutor.remove_dir(local_path)
            return False
        
        try:
            # 4. 切换到开发分支
            if not self.git_service.checkout_branch(local_path, task.code_branch or f"dev-{task_id}"):
                self.logger.error("Failed to checkout branch")
                return False
            
            # 5. 执行开发任务（这里简化处理，实际可能需要LLM参与）
            self.logger.info("Executing development task...")
            # 这里应该根据task.description执行具体的开发工作
            # 暂时模拟创建一个文件
            dev_file_path = f"{local_path}/development_task_{task_id}.md"
            with open(dev_file_path, "w") as f:
                f.write(f"# Development Task {task_id}\n\n")
                f.write(f"Task: {task.title}\n\n")
                f.write(f"Description: {task.description}\n\n")
                f.write("This is a placeholder file created by Numa Avatar.\n")
            
            # 6. 运行测试（简化处理）
            self.logger.info("Running tests...")
            # 这里应该运行项目测试，暂时跳过
            
            # 7. 提交代码
            commit_message = f"feat: Complete development task {task_id} - {task.title}"
            if not self.git_service.commit_changes(local_path, commit_message):
                self.logger.error("Failed to commit changes")
                return False
            
            if not self.git_service.push_changes(local_path, task.code_branch or f"dev-{task_id}"):
                self.logger.error("Failed to push changes")
                return False
            
            # 8. 更新任务状态
            if not self.api_service.update_task_status(task_id, "done"):
                self.logger.error("Failed to update task status")
                return False
            
            self.logger.info(f"Task {task_id} executed successfully")
            return True
        finally:
            # 清理临时目录
            CommandExecutor.remove_dir(local_path)