-- 修复applications表结构
BEGIN TRANSACTION;

-- 1. 创建新表
CREATE TABLE applications_new (
    id INTEGER NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    name VARCHAR,
    description TEXT,
    repository_url VARCHAR,
    status VARCHAR DEFAULT 'created',
    created_by INTEGER,
    owner VARCHAR,
    app_id VARCHAR,
    built_at DATETIME,
    PRIMARY KEY (id),
    FOREIGN KEY(created_by) REFERENCES users (id)
);

-- 2. 复制数据（注意列名映射）
INSERT INTO applications_new (
    id, created_at, updated_at, name, description, repository_url, owner
) 
SELECT 
    id, created_at, updated_at, name, description, git_repo_url, owner
FROM applications;

-- 4. 删除旧表
DROP TABLE applications;

-- 5. 重命名新表
ALTER TABLE applications_new RENAME TO applications;

COMMIT;