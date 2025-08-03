#!/usr/bin/env python3
"""
Qwen CLI 工具 - 用于在工作目录中处理需求内容描述
"""

import argparse
import os
import sys
import json
from typing import Optional

# 添加项目根目录到Python路径
project_root = os.path.join(os.path.dirname(__file__), '..', '..')
sys.path.insert(0, project_root)

# 相对导入
from numa_avatar.mvp.llm.llm_service import LLMService
from numa_avatar.mvp.services.code_service import CodeService
from numa_avatar.mvp.utils.logger import Logger


def load_config() -> dict:
    """加载配置文件"""
    config_path = os.path.join(project_root, 'numa_avatar', 'mvp', 'config.yaml')
    if os.path.exists(config_path):
        import yaml
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    return {}


def get_api_key() -> str:
    """获取API密钥"""
    # 首先检查环境变量
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return api_key
    
    # 然后检查配置文件
    config = load_config()
    api_key = config.get("llm", {}).get("api_key")
    if api_key:
        return api_key
    
    # 如果都没有找到，提示用户输入
    api_key = input("请输入OpenAI API密钥: ")
    return api_key


def process_requirement(requirement: str, working_dir: str, model: str = "gpt-4", temperature: float = 0.7) -> bool:
    """处理需求内容描述
    
    Args:
        requirement: 需求内容描述
        working_dir: 工作目录
        model: 使用的模型
        temperature: 温度参数
        
    Returns:
        是否成功处理
    """
    # 初始化日志服务
    logger = Logger("qwen_cli", os.path.join(working_dir, "logs"))
    logger.info(f"Processing requirement: {requirement}")
    logger.info(f"Working directory: {working_dir}")
    
    try:
        # 获取API密钥
        api_key = get_api_key()
        if not api_key:
            logger.error("No API key provided")
            print("错误: 未提供API密钥", file=sys.stderr)
            return False
        
        # 初始化LLM服务
        llm_service = LLMService(api_key, model, temperature)
        code_service = CodeService(llm_service)
        
        # 记录开始时间
        import time
        start_time = time.time()
        
        # 分析任务
        logger.info("Analyzing requirement")
        print("正在分析需求...")
        task_analysis = code_service.analyze_task(requirement)
        logger.info(f"Task analysis: {task_analysis}")
        
        # 生成代码
        logger.info("Generating code")
        print("正在生成代码...")
        files = code_service.generate_code_files(requirement)
        
        if not files:
            logger.warning("No files generated")
            print("警告: 未生成任何文件")
            return False
        
        logger.info(f"Generated {len(files)} files")
        print(f"生成了 {len(files)} 个文件")
        
        # 写入文件到工作目录
        logger.info("Writing files")
        print("正在写入文件...")
        code_service.write_files(files, working_dir)
        
        # 记录完成时间
        end_time = time.time()
        duration = end_time - start_time
        
        logger.info(f"Requirement processed successfully in {duration:.2f} seconds")
        print(f"需求处理完成，耗时 {duration:.2f} 秒")
        
        return True
    except Exception as e:
        logger.error(f"Error processing requirement: {e}", exc_info=True)
        print(f"错误: 处理需求时发生异常: {e}", file=sys.stderr)
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Qwen CLI - 处理需求内容描述")
    parser.add_argument("requirement", nargs="?", help="需求内容描述")
    parser.add_argument("-p", "--prompt", help="需求内容描述（与位置参数相同）")
    parser.add_argument("-m", "--model", default="gpt-4", help="使用的模型 (默认: gpt-4)")
    parser.add_argument("-t", "--temperature", type=float, default=0.7, help="温度参数 (默认: 0.7)")
    parser.add_argument("-d", "--dir", default=".", help="工作目录 (默认: 当前目录)")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    # 获取需求内容
    requirement = args.prompt or args.requirement
    if not requirement:
        print("错误: 请提供需求内容描述", file=sys.stderr)
        parser.print_help()
        return 1
    
    # 获取工作目录
    working_dir = os.path.abspath(args.dir)
    if not os.path.exists(working_dir):
        print(f"错误: 工作目录不存在: {working_dir}", file=sys.stderr)
        return 1
    
    # 处理需求
    success = process_requirement(
        requirement=requirement,
        working_dir=working_dir,
        model=args.model,
        temperature=args.temperature
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())