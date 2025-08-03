import os
import subprocess
from typing import Optional
from utils.executor import CommandExecutor
from utils.logger import Logger

class GitService:
    """Git操作服务类"""
    
    def __init__(self, username: str = "", email: str = ""):
        self.username = username
        self.email = email
        self.logger = Logger("git_service")
        
        # 配置Git用户信息
        if username:
            self._set_git_config("user.name", username)
        if email:
            self._set_git_config("user.email", email)
    
    def _set_git_config(self, key: str, value: str):
        """设置Git配置
        
        Args:
            key: 配置键
            value: 配置值
        """
        result = CommandExecutor.run_command(["git", "config", "--global", key, value])
        if not result["success"]:
            self.logger.warning(f"Failed to set git config {key}: {result['stderr']}")
    
    def clone_repository(self, repo_url: str, local_path: str) -> bool:
        """克隆代码仓库
        
        Args:
            repo_url: 仓库URL
            local_path: 本地路径
            
        Returns:
            是否成功
        """
        self.logger.info(f"Cloning repository {repo_url} to {local_path}")
        result = CommandExecutor.run_command(["git", "clone", repo_url, local_path])
        
        if result["success"]:
            self.logger.info("Repository cloned successfully")
            return True
        else:
            self.logger.error(f"Failed to clone repository: {result['stderr']}")
            return False
    
    def checkout_branch(self, local_path: str, branch_name: str, create_new: bool = True) -> bool:
        """切换到指定分支
        
        Args:
            local_path: 本地仓库路径
            branch_name: 分支名称
            create_new: 是否创建新分支
            
        Returns:
            是否成功
        """
        self.logger.info(f"Checking out branch {branch_name} in {local_path}")
        
        if create_new:
            # 创建并切换到新分支
            result = CommandExecutor.run_command(["git", "checkout", "-b", branch_name], cwd=local_path)
        else:
            # 切换到现有分支
            result = CommandExecutor.run_command(["git", "checkout", branch_name], cwd=local_path)
        
        if result["success"]:
            self.logger.info(f"Successfully checked out branch {branch_name}")
            return True
        else:
            self.logger.error(f"Failed to checkout branch {branch_name}: {result['stderr']}")
            return False
    
    def commit_changes(self, local_path: str, message: str, files: Optional[list] = None) -> bool:
        """提交代码变更
        
        Args:
            local_path: 本地仓库路径
            message: 提交信息
            files: 要提交的文件列表（默认为所有变更文件）
            
        Returns:
            是否成功
        """
        self.logger.info(f"Committing changes in {local_path}")
        
        try:
            # 添加文件到暂存区
            if files:
                for file in files:
                    result = CommandExecutor.run_command(["git", "add", file], cwd=local_path)
                    if not result["success"]:
                        self.logger.error(f"Failed to add file {file}: {result['stderr']}")
                        return False
            else:
                # 添加所有变更文件
                result = CommandExecutor.run_command(["git", "add", "."], cwd=local_path)
                if not result["success"]:
                    self.logger.error(f"Failed to add files: {result['stderr']}")
                    return False
            
            # 提交更改
            result = CommandExecutor.run_command(["git", "commit", "-m", message], cwd=local_path)
            
            if result["success"]:
                self.logger.info("Changes committed successfully")
                return True
            else:
                # 如果没有变更需要提交，这也被认为是成功的
                if "nothing to commit" in result["stderr"]:
                    self.logger.info("No changes to commit")
                    return True
                self.logger.error(f"Failed to commit changes: {result['stderr']}")
                return False
        except Exception as e:
            self.logger.error(f"Error committing changes: {e}")
            return False
    
    def push_changes(self, local_path: str, branch_name: str) -> bool:
        """推送代码到远程仓库
        
        Args:
            local_path: 本地仓库路径
            branch_name: 分支名称
            
        Returns:
            是否成功
        """
        self.logger.info(f"Pushing changes to branch {branch_name}")
        result = CommandExecutor.run_command(["git", "push", "origin", branch_name], cwd=local_path)
        
        if result["success"]:
            self.logger.info("Changes pushed successfully")
            return True
        else:
            self.logger.error(f"Failed to push changes: {result['stderr']}")
            return False