#!/bin/bash

# 停止前端服务脚本

# 检查PID文件是否存在
if [ ! -f ".frontend_pid" ]; then
    echo "没有找到前端服务PID文件，可能服务未运行"
    
    # 尝试查找并杀死任何运行中的npm start进程
    FRONTEND_PROCESSES=$(ps aux | grep "npm start" | grep -v grep | awk '{print $2}')
    if [ ! -z "$FRONTEND_PROCESSES" ]; then
        echo "发现npm start进程: $FRONTEND_PROCESSES，正在终止..."
        kill $FRONTEND_PROCESSES 2>/dev/null || true
    else
        echo "未发现运行中的npm start进程"
    fi
    
    exit 1
fi

# 读取PID
PID=$(cat .frontend_pid)

# 检查进程是否存在
if ps -p $PID > /dev/null; then
    echo "停止前端服务 (PID: $PID)..."
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
        echo "前端服务已停止"
    fi
else
    echo "进程 $PID 不存在，可能服务已停止"
fi

# 删除PID文件
rm -f .frontend_pid

# 清理前端缓存
echo "清理前端缓存..."
if [ -d "numa_web/node_modules/.cache" ]; then
    rm -rf numa_web/node_modules/.cache
    echo "前端缓存已清理"
fi