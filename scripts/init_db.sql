-- 初始化数据库脚本
-- 创建默认用户、应用和需求

-- 创建默认用户
INSERT INTO users (created_at, updated_at, name, email) VALUES 
  (datetime('now'), datetime('now'), '系统管理员', 'admin@example.com'),
  (datetime('now'), datetime('now'), '开发者', 'dev@example.com'),
  (datetime('now'), datetime('now'), '产品经理', 'pm@example.com');

-- 创建默认应用 (pkb)
INSERT INTO applications (created_at, updated_at, name, description, git_repo_url, owner) VALUES 
  ('2025-08-03 12:00:00', '2025-08-03 12:00:00', 'pkb', '知识库应用', 'https://github.com/example/pkb.git', '产品经理');

-- 创建默认需求 ("添加研究主题")
INSERT INTO requirements (created_at, updated_at, title, description, status, application_id, user_id, clarified) VALUES 
  ('2025-08-03 12:00:00', '2025-08-03 12:00:00', '添加研究主题', '在知识库中添加研究主题功能，允许用户创建、编辑和管理研究主题', 'pending', 1, 3, 0);