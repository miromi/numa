# Numa CLI

Numa CLI 是一个命令行工具，用于与 Numa 后端服务进行交互。

## 安装

1. 安装依赖:
   ```
   pip install -r requirements.txt
   ```

2. 设置环境变量（可选）:
   ```
   export NUMA_API_URL=http://your-api-url
   ```

## 使用方法

### 运行CLI

```
python main.py --help
```

### 需求管理

```
# 创建需求
python main.py requirements create

# 获取指定需求
python main.py requirements get <requirement_id>

# 获取需求列表
python main.py requirements list [--skip SKIP] [--limit LIMIT]
```

### 方案管理

```
# 创建方案
python main.py solutions create

# 获取指定方案
python main.py solutions get <solution_id>

# 获取方案列表
python main.py solutions list [--skip SKIP] [--limit LIMIT]
```

### 开发管理

```
# 创建开发任务
python main.py development create

# 获取指定开发任务
python main.py development get <task_id>

# 获取开发任务列表
python main.py development list [--skip SKIP] [--limit LIMIT]
```

### 部署管理

```
# 创建部署记录
python main.py deployment create

# 获取指定部署记录
python main.py deployment get <deployment_id>

# 获取部署记录列表
python main.py deployment list [--skip SKIP] [--limit LIMIT]
```

### 用户管理

```
# 创建用户
python main.py users create

# 获取指定用户
python main.py users get <user_id>

# 获取用户列表
python main.py users list [--skip SKIP] [--limit LIMIT]
```