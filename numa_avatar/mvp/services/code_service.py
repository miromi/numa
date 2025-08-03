import os
import re
from typing import List, Tuple
from llm.llm_service import LLMService

class CodeService:
    """代码生成服务类"""
    
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service
    
    def generate_code_files(self, task_description: str, project_context: str = "") -> List[Tuple[str, str]]:
        """生成代码文件
        
        Args:
            task_description: 任务描述
            project_context: 项目上下文信息
            
        Returns:
            文件列表，每个元素为(文件名, 文件内容)的元组
        """
        # 使用LLM生成代码
        generated_code = self.llm_service.generate_code(task_description, project_context)
        
        # 解析生成的代码，提取文件名和内容
        files = self._parse_generated_code(generated_code)
        
        return files
    
    def _parse_generated_code(self, generated_code: str) -> List[Tuple[str, str]]:
        """解析生成的代码，提取文件
        
        Args:
            generated_code: LLM生成的代码
            
        Returns:
            文件列表，每个元素为(文件名, 文件内容)的元组
        """
        files = []
        
        # 使用正则表达式匹配文件模式
        pattern = r"FILE:\s*(.*?)\s*CONTENT:\s*(.*?)\s*END_FILE"
        matches = re.findall(pattern, generated_code, re.DOTALL)
        
        for match in matches:
            filename = match[0].strip()
            content = match[1].strip()
            files.append((filename, content))
        
        return files
    
    def write_files(self, files: List[Tuple[str, str]], base_path: str):
        """将文件写入指定目录
        
        Args:
            files: 文件列表，每个元素为(文件名, 文件内容)的元组
            base_path: 基础路径
        """
        for filename, content in files:
            # 确保文件路径存在
            file_path = os.path.join(base_path, filename)
            dir_path = os.path.dirname(file_path)
            
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path)
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Written file: {file_path}")
    
    def analyze_task(self, task_description: str) -> dict:
        """分析任务
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务分析结果
        """
        return self.llm_service.analyze_task(task_description)