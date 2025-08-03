#!/bin/bash

# 初始化开发环境脚本

set -e  # 遇到错误时退出

echo "初始化Numa开发环境..."

# 创建必要的目录
mkdir -p scripts
mkdir -p logs

# 设置环境变量
source scripts/env.sh

# 初始化后端
echo "1. 初始化后端环境..."
cd numa_backend
if [ ! -f "venv/bin/activate" ]; then
    echo "  创建后端虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "  安装后端依赖..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 初始化数据库
echo "  初始化数据库..."
python scripts/init_db.py
cd ..

# 初始化CLI
echo "2. 初始化CLI环境..."
cd numa_cli
if [ ! -f "venv/bin/activate" ]; then
    echo "  创建CLI虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "  安装CLI依赖..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi
cd ..

echo "开发环境初始化完成！"
echo ""
echo "启动环境:"
echo "  ./scripts/start_all.sh"
echo ""
echo "停止环境:"
echo "  ./scripts/stop_all.sh"