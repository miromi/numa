#!/bin/bash

# 启动前端服务脚本

echo "启动前端服务..."

# 创建日志目录（如果不存在）
mkdir -p logs

# 检查前端目录是否存在
if [ ! -d "numa_web" ]; then
    echo "错误: 未找到前端目录 numa_web"
    exit 1
fi

# 进入前端目录
cd numa_web

# 检查是否已安装依赖
if [ ! -d "node_modules" ]; then
    echo "未找到node_modules目录，正在安装依赖..."
    npm install
fi

# 启动前端服务（在后台运行），并将日志重定向到文件
nohup npm start > ../logs/frontend.log 2>&1 &

# 保存PID以便后续停止
echo $! > ../.frontend_pid

echo "前端服务已启动，PID: $(cat ../.frontend_pid)"
echo "前端地址: http://localhost:3000"

# 返回上级目录
cd ..