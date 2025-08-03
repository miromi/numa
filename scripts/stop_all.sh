#!/bin/bash

# 停止整个环境脚本

echo "停止Numa环境..."

# 停止后端服务
if [ -f ".backend_pid" ]; then
    echo "1. 停止后端服务..."
    ./scripts/stop_backend.sh
else
    echo "1. 后端服务未运行"
fi

echo "环境已停止"