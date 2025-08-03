#!/bin/bash

# 数据库迁移脚本 - 添加需求新字段

echo "更新数据库表结构..."

# 进入后端目录
cd numa_backend

# 备份当前数据库
echo "备份当前数据库..."
cp numa.db numa.db.backup.$(date +%Y%m%d_%H%M%S)

# 添加新字段到requirements表
echo "添加新字段到requirements表..."
sqlite3 numa.db <<EOF
ALTER TABLE requirements ADD COLUMN assigned_to INTEGER REFERENCES users(id);
ALTER TABLE requirements ADD COLUMN branch_name TEXT;
ALTER TABLE requirements ADD COLUMN spec_document TEXT;
EOF

echo "数据库表结构更新完成！"

# 返回上级目录
cd ..