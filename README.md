# Numa

Numa 是一个自动化 DevOps 流程工具，能够自动完成需求分析、方案设计、编码实现、测试和部署的整个流程。

## 项目结构

- `docs/` - 文档目录
- `numa_backend/` - 后端服务代码
- `numa_cli/` - 命令行界面代码
- `scripts/` - 环境管理和部署脚本

## 环境要求

- Python 3.8+
- pip

## 快速开始

### 1. 初始化开发环境

```bash
./scripts/init_dev_env.sh
```

### 2. 启动环境

```bash
./scripts/start_all.sh
```

### 3. 使用CLI

```bash
cd numa_cli
source venv/bin/activate
python main.py --help
```

### 4. 停止环境

```bash
./scripts/stop_all.sh
```

## 后端API

后端服务启动后，可以通过以下地址访问：

- API地址: http://localhost:8000
- API文档: http://localhost:8000/docs

## 开发指南

### 后端开发

后端使用 Python + FastAPI 构建，数据库使用 SQLite。

### CLI开发

CLI使用 Python + Click 构建，通过 HTTP 与后端 API 交互。