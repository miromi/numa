# Numa Web Interface

Numa Web Interface 是自动化DevOps流程工具的图形化界面，提供了直观的用户界面来管理需求、方案、开发任务和部署。

## 技术栈

- React.js 17
- Material-UI
- Axios (HTTP客户端)
- React Router (路由管理)

## 目录结构

```
src/
  components/     # 可复用的UI组件
  pages/          # 页面组件
  services/       # API服务封装
  utils/          # 工具函数
  assets/         # 静态资源
  contexts/       # React Context
```

## 开发环境搭建

1. 安装依赖:
   ```
   npm install
   ```

2. 启动开发服务器:
   ```
   npm start
   ```

3. 构建生产版本:
   ```
   npm run build
   ```

## 页面功能

### 1. 首页 (Dashboard)
- 系统概览
- 快捷操作入口

### 2. 需求管理
- 需求列表
- 创建/编辑需求
- 需求详情

### 3. 方案管理
- 方案列表
- 创建/编辑方案
- 方案详情

### 4. 开发管理
- 开发任务列表
- 创建/编辑开发任务
- 开发任务详情

### 5. 部署管理
- 部署记录列表
- 创建/编辑部署记录
- 部署详情

## API集成

前端通过RESTful API与后端服务通信，API地址配置在`src/services/api.js`中。