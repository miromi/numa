#!/usr/bin/env python3
"""
安装脚本 - 将qwen命令安装到系统中
"""

import os
import sys
import shutil
from pathlib import Path

def install_qwen_cli():
    """安装qwen CLI工具"""
    # 获取当前脚本目录
    current_dir = Path(__file__).parent.absolute()
    project_root = current_dir.parent
    
    # qwen.py的路径
    qwen_script = current_dir / "qwen.py"
    
    # 检查qwen.py是否存在
    if not qwen_script.exists():
        print(f"错误: 找不到 {qwen_script}", file=sys.stderr)
        return False
    
    # 确定安装目录
    # 优先使用 ~/bin，如果不存在则使用 /usr/local/bin
    home_bin = Path.home() / "bin"
    if home_bin.exists():
        install_dir = home_bin
    else:
        install_dir = Path("/usr/local/bin")
    
    # 检查安装目录是否存在且可写
    if not install_dir.exists():
        try:
            install_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"错误: 无法创建安装目录 {install_dir}: {e}", file=sys.stderr)
            return False
    
    if not os.access(install_dir, os.W_OK):
        print(f"错误: 没有写入权限 {install_dir}", file=sys.stderr)
        print("请使用 sudo 运行此脚本，或选择其他安装目录", file=sys.stderr)
        return False
    
    # 目标路径
    target_path = install_dir / "qwen"
    
    try:
        # 复制文件
        shutil.copy2(qwen_script, target_path)
        
        # 设置执行权限
        os.chmod(target_path, 0o755)
        
        print(f"成功安装 qwen 到 {target_path}")
        print(f"现在可以在任何目录中使用 'qwen' 命令")
        print(f"示例: cd working_directory && qwen -p '需求内容描述'")
        
        return True
    except Exception as e:
        print(f"错误: 安装失败: {e}", file=sys.stderr)
        return False


def uninstall_qwen_cli():
    """卸载qwen CLI工具"""
    # 确定安装目录
    home_bin = Path.home() / "bin"
    system_bin = Path("/usr/local/bin")
    
    # 检查可能的安装位置
    possible_paths = [
        home_bin / "qwen",
        system_bin / "qwen"
    ]
    
    uninstalled = False
    for path in possible_paths:
        if path.exists():
            try:
                path.unlink()
                print(f"已卸载 {path}")
                uninstalled = True
            except Exception as e:
                print(f"错误: 无法卸载 {path}: {e}", file=sys.stderr)
    
    if not uninstalled:
        print("未找到已安装的 qwen 命令")
        return False
    
    return True


def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "uninstall":
        return 0 if uninstall_qwen_cli() else 1
    else:
        return 0 if install_qwen_cli() else 1


if __name__ == "__main__":
    sys.exit(main())