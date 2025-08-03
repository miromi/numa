-- 初始化数据库脚本
-- 创建默认用户、应用和需求

-- 创建默认用户
INSERT INTO users (created_at, updated_at, name, email) VALUES 
  ('2025-08-03 04:05:00', '2025-08-03 04:05:00', '系统管理员', 'admin@example.com'),
  ('2025-08-03 04:05:00', '2025-08-03 04:05:00', '开发者', 'dev@example.com'),
  ('2025-08-03 04:05:00', '2025-08-03 04:05:00', '产品经理', 'pm@example.com');

-- 创建默认应用 (pkb)
INSERT INTO applications (created_at, updated_at, name, description, git_repo_url, owner) VALUES 
  ('2025-08-03 04:08:01', '2025-08-03 04:08:01', 'pkb', 'personal knownedge base', 'git@github.com:miromi/pkb.git', 'yao');

-- 创建默认需求 ("添加研究主题")
INSERT INTO requirements (created_at, updated_at, title, description, status, application_id, assigned_to, branch_name, spec_document, clarified) VALUES 
  ('2025-08-03 04:09:19', '2025-08-03 04:49:32', '添加"研究主题"', '研究主题：对新获得的数据、信息、知识 进行学习、研究，反应到对研究主题的知识的更新', 'confirmed', 1, 1, 'req-2-添加"研究主题"', '# 需求规范文档

## 需求标题
添加"研究主题"

## 需求描述
研究主题：对新获得的数据、信息、知识 进行学习、研究，反应到对研究主题的知识的更新

## 自动生成的澄清问题
1. 请确认该需求的优先级是高、中还是低？
2. 该需求是否需要在特定时间点前完成？
3. 是否有其他相关的功能或需求需要考虑？

## 下一步行动
请回答以上问题，以便我们继续进行需求开发。
', 0);