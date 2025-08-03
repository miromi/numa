from openai import OpenAI
from typing import List, Dict, Any, Optional
import json

class LLMService:
    """LLM服务类"""
    
    def __init__(self, api_key: str, model: str = "gpt-4", temperature: float = 0.7):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
    
    def generate_code(self, task_description: str, project_context: str = "") -> str:
        """根据任务描述生成代码
        
        Args:
            task_description: 任务描述
            project_context: 项目上下文信息
            
        Returns:
            生成的代码
        """
        # 检查API密钥是否有效
        if not self.client.api_key or self.client.api_key == "your_openai_api_key_here":
            # 返回模拟的代码生成结果
            return """FILE: app.py
CONTENT:
#!/usr/bin/env python3

def hello_world():
    return "Hello, World!"

if __name__ == "__main__":
    print(hello_world())
END_FILE"""
        
        prompt = f"""
        你是一个专业的软件开发工程师。请根据以下任务描述生成相应的代码。

        任务描述:
        {task_description}

        项目上下文:
        {project_context}

        请生成完整的、可运行的代码。如果任务涉及创建新文件，请提供文件名和完整内容。
        如果任务涉及修改现有文件，请指出需要修改的部分并提供修改后的内容。

        请严格按照以下格式输出:
        FILE: <文件名>
        CONTENT:
        <文件内容>
        END_FILE

        如果有多个文件，请重复上述格式。
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的软件开发工程师，擅长根据需求生成高质量代码。"},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            max_tokens=2000
        )
        
        return response.choices[0].message.content
    
    def analyze_task(self, task_description: str) -> Dict[str, Any]:
        """分析任务描述，提取关键信息
        
        Args:
            task_description: 任务描述
            
        Returns:
            任务分析结果
        """
        # 检查API密钥是否有效
        if not self.client.api_key or self.client.api_key == "your_openai_api_key_here":
            # 返回模拟的任务分析结果
            return {
                "functional_requirements": ["实现一个简单的Hello World功能"],
                "technical_requirements": ["使用Python 3.x"],
                "files_to_create": ["app.py"],
                "files_to_modify": [],
                "estimated_complexity": "简单"
            }
        
        prompt = f"""
        请分析以下任务描述，提取关键信息并结构化输出：

        任务描述:
        {task_description}

        请按照以下JSON格式输出分析结果:
        {{
            "functional_requirements": ["功能需求列表"],
            "technical_requirements": ["技术需求列表"],
            "files_to_create": ["需要创建的文件列表"],
            "files_to_modify": ["需要修改的文件列表"],
            "estimated_complexity": "任务复杂度（简单/中等/复杂）"
        }}
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的软件开发工程师，擅长分析任务需求。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # 使用较低的温度以获得更一致的结果
            response_format={"type": "json_object"}
        )
        
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            # 如果解析失败，返回默认结构
            return {
                "functional_requirements": [],
                "technical_requirements": [],
                "files_to_create": [],
                "files_to_modify": [],
                "estimated_complexity": "未知"
            }
    
    def fix_code(self, error_message: str, code: str) -> str:
        """修复有错误的代码
        
        Args:
            error_message: 错误信息
            code: 有错误的代码
            
        Returns:
            修复后的代码
        """
        prompt = f"""
        以下代码存在错误，请修复它：

        错误信息:
        {error_message}

        代码:
        {code}

        请提供修复后的完整代码。
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个专业的软件开发工程师，擅长调试和修复代码。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500
        )
        
        return response.choices[0].message.content