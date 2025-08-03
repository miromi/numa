import subprocess
import os
import tempfile
import shutil
from typing import List, Optional

class CommandExecutor:
    """命令执行工具类"""
    
    @staticmethod
    def run_command(command: List[str], cwd: Optional[str] = None, timeout: int = 300) -> dict:
        """执行命令
        
        Args:
            command: 命令列表
            cwd: 工作目录
            timeout: 超时时间（秒）
            
        Returns:
            包含执行结果的字典
        """
        try:
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    @staticmethod
    def create_temp_dir(prefix: str = "numa_") -> str:
        """创建临时目录
        
        Args:
            prefix: 目录前缀
            
        Returns:
            临时目录路径
        """
        return tempfile.mkdtemp(prefix=prefix)
    
    @staticmethod
    def remove_dir(path: str) -> bool:
        """删除目录
        
        Args:
            path: 目录路径
            
        Returns:
            是否成功
        """
        try:
            if os.path.exists(path):
                shutil.rmtree(path)
            return True
        except Exception as e:
            print(f"Failed to remove directory {path}: {e}")
            return False