import os
import sys
from avatar import Avatar
from llm.llm_service import LLMService
from services.code_service import CodeService

def test_llm_service():
    """测试LLM服务"""
    print("Testing LLM Service...")
    
    # 从环境变量获取API密钥
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY environment variable not set")
        return
    
    llm_service = LLMService(api_key=api_key)
    
    # 测试任务分析
    task_description = "实现一个用户登录功能，包括前端表单和后端验证接口"
    analysis = llm_service.analyze_task(task_description)
    print(f"Task Analysis: {analysis}")
    
    # 测试代码生成
    code = llm_service.generate_code(task_description)
    print(f"Generated Code: {code}")

def test_code_service():
    """测试代码服务"""
    print("\nTesting Code Service...")
    
    # 从环境变量获取API密钥
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY environment variable not set")
        return
    
    llm_service = LLMService(api_key=api_key)
    code_service = CodeService(llm_service)
    
    # 测试任务分析
    task_description = "创建一个简单的Python Flask应用，包含一个返回'Hello, World!'的路由"
    analysis = code_service.analyze_task(task_description)
    print(f"Task Analysis: {analysis}")
    
    # 测试代码生成
    files = code_service.generate_code_files(task_description)
    print(f"Generated Files: {files}")

def test_avatar():
    """测试Avatar"""
    print("\nTesting Avatar...")
    avatar = Avatar()
    status = avatar.get_status()
    print(f"Avatar Status: {status}")

if __name__ == "__main__":
    # 添加当前目录到Python路径
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    
    # 运行测试
    test_llm_service()
    test_code_service()
    test_avatar()
    
    print("\nAll tests completed!")