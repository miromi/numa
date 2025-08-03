#!/bin/bash

# 停止整个环境脚本

echo "停止Numa环境..."

# 停止前端服务
if [ -f ".frontend_pid" ]; then
    echo "1. 停止前端服务..."
    ./scripts/stop_frontend.sh
else
    echo "1. 前端服务未运行"
fi

# 停止后端服务
if [ -f ".backend_pid" ]; then
    echo "2. 停止后端服务..."
    ./scripts/stop_backend.sh
else
    echo "2. 后端服务未运行"
fi

# 如果stop_backend.sh未能停止服务，强制杀死相关进程
echo "3. 检查是否有残留的后端进程..."
BACKEND_PROCESSES=$(ps aux | grep "uvicorn main:app" | grep -v grep | awk '{print $2}')
if [ ! -z "$BACKEND_PROCESSES" ]; then
    echo "发现残留的后端进程: $BACKEND_PROCESSES，正在强制终止..."
    kill -9 $BACKEND_PROCESSES 2>/dev/null || true
else
    echo "未发现残留的后端进程"
fi

# 清理PID文件（如果存在）
if [ -f ".backend_pid" ]; then
    rm .backend_pid
    echo "已清理后端PID文件"
fi

if [ -f ".frontend_pid" ]; then
    rm .frontend_pid
    echo "已清理前端PID文件"
fi

echo "环境已停止"