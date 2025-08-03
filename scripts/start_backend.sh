#!/bin/bash

# 启动后端服务脚本

echo "启动后端服务..."

# 创建日志目录（如果不存在）
mkdir -p logs

# 启动后端服务
cd numa_backend
source venv/bin/activate

# 启动后端服务（在后台运行），并将日志重定向到文件
nohup uvicorn main:app --reload --host 0.0.0.0 --port 7301 > ../logs/backend.log 2>&1 &

# 保存PID以便后续停止
echo $! > ../.backend_pid

echo "后端服务已启动，PID: $(cat ../.backend_pid)"
echo "API地址: http://localhost:7301"
echo "API文档: http://localhost:7301/docs"

# 返回上级目录
cd ..