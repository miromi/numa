#!/bin/bash

# 停止前端服务脚本

# 检查PID文件是否存在
if [ ! -f ".frontend_pid" ]; then
    echo "没有找到前端服务PID文件，可能服务未运行"
    exit 1
fi

# 读取PID
PID=$(cat .frontend_pid)

# 检查进程是否存在
if ps -p $PID > /dev/null; then
    echo "停止前端服务 (PID: $PID)..."
    kill $PID
    
    # 等待进程结束
    while ps -p $PID > /dev/null; do
        sleep 1
    done
    
    echo "前端服务已停止"
else
    echo "进程 $PID 不存在，可能服务已停止"
fi

# 删除PID文件
rm .frontend_pid