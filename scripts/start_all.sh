#!/bin/bash

# 启动整个环境脚本

set -e  # 遇到错误时退出

echo "启动Numa环境..."

# 启动后端服务
echo "1. 启动后端服务..."
./scripts/start_backend.sh

# 等待后端服务启动
sleep 5

# 启动前端服务
echo "2. 启动前端服务..."
./scripts/start_frontend.sh

# 等待前端服务启动
sleep 5

# 启动CLI环境
echo "3. 准备CLI环境..."
./scripts/start_cli.sh

echo "环境启动完成！"
echo "后端API地址: http://localhost:8000"
echo "API文档地址: http://localhost:8000/docs"
echo "前端地址: http://localhost:3000"
echo ""
echo "使用CLI:"
echo "  cd numa_cli && source venv/bin/activate"
echo "  python main.py --help"