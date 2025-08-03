#!/bin/bash

# 清理开发环境缓存脚本

echo "清理开发环境缓存..."

# 清理前端缓存
if [ -d "numa_web/node_modules/.cache" ]; then
    echo "清理前端缓存..."
    rm -rf numa_web/node_modules/.cache
fi

# 清理后端Python缓存
echo "清理后端Python缓存..."
find numa_backend -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find numa_backend -type f -name "*.pyc" -delete 2>/dev/null || true

# 清理CLI Python缓存
echo "清理CLI Python缓存..."
find numa_cli -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find numa_cli -type f -name "*.pyc" -delete 2>/dev/null || true

echo "缓存清理完成！"