#!/bin/bash

# 停止后端服务脚本

# 检查PID文件是否存在
if [ ! -f ".backend_pid" ]; then
    echo "没有找到后端服务PID文件，可能服务未运行"
    exit 1
fi

# 读取PID
PID=$(cat .backend_pid)

# 检查进程是否存在
if ps -p $PID > /dev/null; then
    echo "停止后端服务 (PID: $PID)..."
    kill $PID
    
    # 等待进程结束，最多等待10秒
    COUNT=0
    while ps -p $PID > /dev/null && [ $COUNT -lt 10 ]; do
        sleep 1
        COUNT=$((COUNT + 1))
    done
    
    # 如果进程仍未结束，强制杀死
    if ps -p $PID > /dev/null; then
        echo "进程未正常结束，正在强制终止..."
        kill -9 $PID 2>/dev/null || true
    else
        echo "后端服务已停止"
    fi
else
    echo "进程 $PID 不存在，可能服务已停止"
fi

# 删除PID文件
rm -f .backend_pid