# Numa Avatar API 文档

## 概述

Numa Avatar 通过与 Numa Backend 的 API 进行交互来获取任务、更新状态和上报日志。

## 后端API接口（Numa-Backend提供）

### 消息订阅相关

#### GET /api/topics/tasks
获取任务消息topic

**响应示例**：
```json
{
  "id": 1,
  "name": "tasks",
  "description": "Development tasks topic"
}
```

#### GET /api/topics/{topic_id}/messages
从topic获取消息

**响应示例**：
```json
{
  "data": [
    {
      "id": 1,
      "topic_id": 1,
      "data": {
        "task_id": 123
      },
      "created_at": "2025-08-03T10:00:00Z"
    }
  ]
}
```

### 任务相关

#### GET /api/tasks/{task_id}
获取任务详情

**响应示例**：
```json
{
  "id": 123,
  "title": "实现用户登录功能",
  "description": "开发用户登录页面和后端接口",
  "status": "todo",
  "assigned_to": 1,
  "code_branch": "dev-123-user-login",
  "solution_id": 456,
  "requirement_id": 789,
  "application_id": 1,
  "started_at": null,
  "completed_at": null
}
```

#### PUT /api/tasks/{task_id}/status
更新任务状态

**请求体**：
```json
{
  "status": "done"
}
```

**响应示例**：
```json
{
  "id": 123,
  "title": "实现用户登录功能",
  "status": "done",
  // ... 其他字段
}
```

#### POST /api/tasks/{task_id}/logs
上报执行日志

**请求体**：
```json
{
  "logs": "2025-08-03 10:00:00 - 开始执行任务\n2025-08-03 10:05:00 - 克隆代码仓库完成"
}
```

**响应示例**：
```json
{
  "success": true
}
```

### Git相关

#### GET /api/applications/{app_id}
获取应用信息（包含Git仓库地址）

**响应示例**：
```json
{
  "id": 1,
  "name": "my-app",
  "description": "My application",
  "git_repo_url": "https://github.com/user/my-app.git",
  "owner": "user"
}
```

## Avatar内部接口

### GET /status
获取Avatar运行状态

**响应示例**：
```json
{
  "status": "running",
  "avatar_id": "avatar_001",
  "avatar_name": "Developer Avatar"
}
```

### POST /config
更新配置信息

**请求体**：
```json
{
  "backend": {
    "url": "http://new-backend:7301"
  }
}
```

**响应示例**：
```json
{
  "success": true
}
```