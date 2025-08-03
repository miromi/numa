#!/bin/bash

# 清理数据库脚本

echo "清理数据库..."

# 进入后端目录
cd numa_backend

# 备份当前数据库
echo "备份当前数据库..."
cp numa.db numa.db.backup.$(date +%Y%m%d_%H%M%S)

# 删除所有表数据
echo "清理所有表数据..."
sqlite3 numa.db <<EOF
DELETE FROM applications;
DELETE FROM deployments;
DELETE FROM development_tasks;
DELETE FROM solutions;
DELETE FROM requirements;
DELETE FROM users;
EOF

# 重置自增ID
echo "重置自增ID..."
sqlite3 numa.db <<EOF
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'applications';
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'deployments';
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'development_tasks';
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'solutions';
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'requirements';
UPDATE sqlite_sequence SET seq = 0 WHERE name = 'users';
EOF

echo "数据库清理完成！"

# 返回上级目录
cd ..