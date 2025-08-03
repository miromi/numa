# Numa 后端 API 文档

本文档详细描述了 Numa 后端服务提供的所有 API 接口。API 采用 RESTful 设计风格，使用 JSON 作为数据交换格式。

## 基础信息

- **API 根路径**: `http://localhost:8000/api`
- **API 版本**: v1
- **数据格式**: JSON
- **认证方式**: (待定义)

## 错误响应格式

所有错误响应都遵循以下格式：

```json
{
  "detail": "错误描述信息"
}
```

## 1. 需求管理模块

### 1.1 创建需求

- **URL**: `POST /v1/requirements/`
- **请求数据**:
  ```json
  {
    "title": "需求标题",
    "description": "需求详细描述",
    "user_id": 1
  }
  ```
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "title": "需求标题",
    "description": "需求详细描述",
    "status": "pending",
    "user_id": 1
  }
  ```
- **状态码**:
  - 200: 成功创建
  - 422: 请求数据验证失败

### 1.2 获取单个需求

- **URL**: `GET /v1/requirements/{requirement_id}`
- **路径参数**:
  - `requirement_id`: 需求ID
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "title": "需求标题",
    "description": "需求详细描述",
    "status": "pending",
    "user_id": 1
  }
  ```
- **状态码**:
  - 200: 成功获取
  - 404: 需求不存在

### 1.3 获取需求列表

- **URL**: `GET /v1/requirements/`
- **查询参数**:
  - `skip`: 跳过的记录数，默认为0
  - `limit`: 返回的记录数，默认为100，最大为1000
- **响应数据**:
  ```json
  [
    {
      "id": 1,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": null,
      "title": "需求标题",
      "description": "需求详细描述",
      "status": "pending",
      "user_id": 1
    }
  ]
  ```
- **状态码**:
  - 200: 成功获取

## 2. 方案管理模块

### 2.1 创建方案

- **URL**: `POST /v1/solutions/`
- **请求数据**:
  ```json
  {
    "title": "方案标题",
    "description": "方案详细描述",
    "requirement_id": 1
  }
  ```
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "title": "方案标题",
    "description": "方案详细描述",
    "status": "proposed",
    "requirement_id": 1
  }
  ```
- **状态码**:
  - 200: 成功创建
  - 422: 请求数据验证失败

### 2.2 获取单个方案

- **URL**: `GET /v1/solutions/{solution_id}`
- **路径参数**:
  - `solution_id`: 方案ID
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "title": "方案标题",
    "description": "方案详细描述",
    "status": "proposed",
    "requirement_id": 1
  }
  ```
- **状态码**:
  - 200: 成功获取
  - 404: 方案不存在

### 2.3 获取方案列表

- **URL**: `GET /v1/solutions/`
- **查询参数**:
  - `skip`: 跳过的记录数，默认为0
  - `limit`: 返回的记录数，默认为100，最大为1000
- **响应数据**:
  ```json
  [
    {
      "id": 1,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": null,
      "title": "方案标题",
      "description": "方案详细描述",
      "status": "proposed",
      "requirement_id": 1
    }
  ]
  ```
- **状态码**:
  - 200: 成功获取

## 3. 开发管理模块

### 3.1 创建开发任务

- **URL**: `POST /v1/development/`
- **请求数据**:
  ```json
  {
    "title": "开发任务标题",
    "description": "开发任务详细描述",
    "solution_id": 1,
    "assigned_to": 1
  }
  ```
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "title": "开发任务标题",
    "description": "开发任务详细描述",
    "status": "todo",
    "solution_id": 1,
    "assigned_to": 1,
    "started_at": null,
    "completed_at": null
  }
  ```
- **状态码**:
  - 200: 成功创建
  - 422: 请求数据验证失败

### 3.2 获取单个开发任务

- **URL**: `GET /v1/development/{task_id}`
- **路径参数**:
  - `task_id`: 开发任务ID
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "title": "开发任务标题",
    "description": "开发任务详细描述",
    "status": "todo",
    "solution_id": 1,
    "assigned_to": 1,
    "started_at": null,
    "completed_at": null
  }
  ```
- **状态码**:
  - 200: 成功获取
  - 404: 开发任务不存在

### 3.3 获取开发任务列表

- **URL**: `GET /v1/development/`
- **查询参数**:
  - `skip`: 跳过的记录数，默认为0
  - `limit`: 返回的记录数，默认为100，最大为1000
- **响应数据**:
  ```json
  [
    {
      "id": 1,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": null,
      "title": "开发任务标题",
      "description": "开发任务详细描述",
      "status": "todo",
      "solution_id": 1,
      "assigned_to": 1,
      "started_at": null,
      "completed_at": null
    }
  ]
  ```
- **状态码**:
  - 200: 成功获取

## 4. 部署管理模块

### 4.1 创建部署记录

- **URL**: `POST /v1/deployment/`
- **请求数据**:
  ```json
  {
    "name": "部署名称",
    "description": "部署详细描述",
    "development_task_id": 1,
    "deployed_by": 1
  }
  ```
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "name": "部署名称",
    "description": "部署详细描述",
    "status": "pending",
    "development_task_id": 1,
    "deployed_by": 1,
    "deployed_at": null
  }
  ```
- **状态码**:
  - 200: 成功创建
  - 422: 请求数据验证失败

### 4.2 获取单个部署记录

- **URL**: `GET /v1/deployment/{deployment_id}`
- **路径参数**:
  - `deployment_id`: 部署记录ID
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "name": "部署名称",
    "description": "部署详细描述",
    "status": "pending",
    "development_task_id": 1,
    "deployed_by": 1,
    "deployed_at": null
  }
  ```
- **状态码**:
  - 200: 成功获取
  - 404: 部署记录不存在

### 4.3 获取部署记录列表

- **URL**: `GET /v1/deployment/`
- **查询参数**:
  - `skip`: 跳过的记录数，默认为0
  - `limit`: 返回的记录数，默认为100，最大为1000
- **响应数据**:
  ```json
  [
    {
      "id": 1,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": null,
      "name": "部署名称",
      "description": "部署详细描述",
      "status": "pending",
      "development_task_id": 1,
      "deployed_by": 1,
      "deployed_at": null
    }
  ]
  ```
- **状态码**:
  - 200: 成功获取

## 5. 用户管理模块

### 5.1 创建用户

- **URL**: `POST /v1/users/`
- **请求数据**:
  ```json
  {
    "name": "用户姓名",
    "email": "user@example.com"
  }
  ```
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "name": "用户姓名",
    "email": "user@example.com"
  }
  ```
- **状态码**:
  - 200: 成功创建
  - 422: 请求数据验证失败

### 5.2 获取单个用户

- **URL**: `GET /v1/users/{user_id}`
- **路径参数**:
  - `user_id`: 用户ID
- **响应数据**:
  ```json
  {
    "id": 1,
    "created_at": "2023-01-01T00:00:00",
    "updated_at": null,
    "name": "用户姓名",
    "email": "user@example.com"
  }
  ```
- **状态码**:
  - 200: 成功获取
  - 404: 用户不存在

### 5.3 获取用户列表

- **URL**: `GET /v1/users/`
- **查询参数**:
  - `skip`: 跳过的记录数，默认为0
  - `limit`: 返回的记录数，默认为100，最大为1000
- **响应数据**:
  ```json
  [
    {
      "id": 1,
      "created_at": "2023-01-01T00:00:00",
      "updated_at": null,
      "name": "用户姓名",
      "email": "user@example.com"
    }
  ]
  ```
- **状态码**:
  - 200: 成功获取