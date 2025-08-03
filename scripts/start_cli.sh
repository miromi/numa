#!/bin/bash

# 启动CLI环境脚本

set -e  # 遇到错误时退出

# 检查是否在项目根目录
if [ ! -d "numa_cli" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 进入CLI目录
cd numa_cli

# 检查是否已经安装了依赖
if [ ! -f "venv/bin/activate" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "安装依赖..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

echo "CLI环境已准备就绪"
echo "使用方法: python main.py --help"