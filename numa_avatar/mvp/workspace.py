import os
import shutil
import json
from typing import Optional
from datetime import datetime

class WorkspaceManager:
    """工作区管理类"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path
        self.repos_path = os.path.join(workspace_path, "repos")
        self.temp_path = os.path.join(workspace_path, "temp")
        self.logs_path = os.path.join(workspace_path, "logs")
        self.cache_path = os.path.join(workspace_path, "cache")
        self.config_path = os.path.join(workspace_path, "config")
        
        # 初始化工作区目录
        self._init_workspace()
    
    def _init_workspace(self):
        """初始化工作区目录结构"""
        dirs = [
            self.workspace_path,
            self.repos_path,
            self.temp_path,
            self.logs_path,
            self.cache_path,
            self.config_path
        ]
        
        for dir_path in dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
        
        # 创建workspace.json记录工作区信息
        workspace_info = {
            "created_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        workspace_info_file = os.path.join(self.workspace_path, "workspace.json")
        if not os.path.exists(workspace_info_file):
            with open(workspace_info_file, 'w') as f:
                json.dump(workspace_info, f, indent=2)
    
    def get_repo_path(self, repo_id: str) -> str:
        """获取仓库路径"""
        return os.path.join(self.repos_path, repo_id)
    
    def get_temp_path(self, task_id: str) -> str:
        """获取任务临时路径"""
        task_temp_path = os.path.join(self.temp_path, f"task_{task_id}")
        if not os.path.exists(task_temp_path):
            os.makedirs(task_temp_path, exist_ok=True)
        return task_temp_path
    
    def get_log_file(self, task_id: Optional[str] = None) -> str:
        """获取日志文件路径"""
        if task_id:
            task_log_dir = os.path.join(self.logs_path, "task_logs")
            if not os.path.exists(task_log_dir):
                os.makedirs(task_log_dir, exist_ok=True)
            return os.path.join(task_log_dir, f"task_{task_id}.log")
        else:
            return os.path.join(self.logs_path, "avatar.log")
    
    def get_cache_file(self, cache_key: str) -> str:
        """获取缓存文件路径"""
        return os.path.join(self.cache_path, f"{cache_key}.cache")
    
    def cleanup_temp(self, task_id: Optional[str] = None):
        """清理临时文件"""
        if task_id:
            task_temp_path = os.path.join(self.temp_path, f"task_{task_id}")
            if os.path.exists(task_temp_path):
                shutil.rmtree(task_temp_path)
        else:
            # 清理所有临时文件
            if os.path.exists(self.temp_path):
                for item in os.listdir(self.temp_path):
                    item_path = os.path.join(self.temp_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)
    
    def get_workspace_info(self) -> dict:
        """获取工作区信息"""
        workspace_info_file = os.path.join(self.workspace_path, "workspace.json")
        if os.path.exists(workspace_info_file):
            with open(workspace_info_file, 'r') as f:
                return json.load(f)
        return {}
    
    def is_valid_workspace(self) -> bool:
        """检查是否为有效的工作区"""
        workspace_info_file = os.path.join(self.workspace_path, "workspace.json")
        return os.path.exists(workspace_info_file)