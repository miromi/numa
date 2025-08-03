#!/bin/bash

# 启动后端服务脚本

set -e  # 遇到错误时退出

# 检查是否在项目根目录
if [ ! -d "numa_backend" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 进入后端目录
cd numa_backend

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

# 启动服务
echo "启动后端服务..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &

# 记录进程ID
echo $! > ../.backend_pid

echo "后端服务已启动，PID: $(cat ../.backend_pid)"
echo "API地址: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"