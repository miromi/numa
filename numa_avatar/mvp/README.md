# Numa Avatar MVP

这是一个简化版本的Numa Avatar，集成了LLM功能，用于代码生成和任务执行。

## 功能特性

1. **LLM集成**：与OpenAI GPT模型集成
2. **后端通信**：与Numa Backend进行消息订阅和API通信
3. **任务解析**：解析来自后端的任务描述
4. **代码生成**：根据任务描述生成代码
5. **Git操作**：基本的Git操作（克隆、提交、推送）
6. **详细日志记录**：记录任务执行过程中的详细信息
7. **工作区管理**：管理代码仓库、临时文件、日志和缓存
8. **测试执行**：运行项目测试
9. **命令行工具**：提供CLI方式直接处理需求

## 目录结构

```
mvp/
├── main.py              # 入口文件
├── config.py            # 配置管理
├── avatar.py            # Avatar主类
├── workspace.py         # 工作区管理
├── llm/
│   └── llm_service.py   # LLM服务
├── services/
│   ├── api_service.py   # API服务
│   ├── code_service.py  # 代码生成服务
│   ├── git_service.py   # Git操作服务
│   └── message_service.py # 消息订阅服务
├── utils/
│   ├── executor.py      # 命令执行工具
│   └── logger.py        # 日志服务
├── cli/                 # 命令行工具
│   ├── qwen.py          # Qwen CLI工具
│   ├── install.py       # 安装脚本
│   └── README.md        # CLI使用说明
└── tests/               # 测试用例
    ├── test_llm_service.py
    ├── test_code_service.py
    ├── test_git_service.py
    ├── test_avatar.py
    ├── test_api_service.py
    ├── test_message_service.py
    ├── test_executor.py
    ├── test_workspace.py
    ├── test_logger.py
    ├── __init__.py
    └── run_tests.py     # 运行所有测试的脚本
```

## 日志结构

```
/logs/
├── avatar.log           # Avatar主日志
├── tasks/               # 任务日志目录
│   ├── task_123.log     # 特定任务日志
│   └── task_456.log     # 特定任务日志
```

## 配置说明

在`config.yaml`中配置以下参数：

```yaml
backend:
  url: "http://localhost:7301"    # 后端API地址
  api_token: "your_api_token"     # API认证令牌

git:
  username: "your_git_username"   # Git用户名
  email: "your_email@example.com" # Git邮箱

avatar:
  id: "avatar_mvp_001"            # Avatar ID
  name: "Developer Avatar MVP"    # Avatar名称
  workspace: "./workspace"        # 工作区路径
  topic_name: "tasks"             # 订阅的topic名称
  log_dir: "./logs"               # 日志目录路径

llm:
  api_key: "your_openai_api_key"  # OpenAI API密钥
  model: "gpt-4"                  # 使用的模型
  temperature: 0.7                # 温度参数

polling:
  interval: 5                     # 轮询间隔（秒）
```

## 快速开始

### 运行Avatar

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 配置环境变量（可选，也可以在config.yaml中配置）：
   ```
   export OPENAI_API_KEY=your_openai_api_key
   ```

3. 配置config.yaml文件

4. 运行Avatar：
   ```
   python main.py
   ```

### 使用CLI工具

1. 安装CLI工具：
   ```
   cd cli
   python install.py
   ```

2. 在工作目录中使用：
   ```
   cd working_directory
   qwen -p "需求内容描述"
   ```

## 运行测试

1. 运行所有测试：
   ```
   python run_tests.py
   ```

2. 运行单个测试文件：
   ```
   python -m unittest tests.test_api_service
   ```

3. 运行特定测试方法：
   ```
   python -m unittest tests.test_api_service.TestAPIService.test_get_task
   ```