# Qwen CLI 工具

Qwen CLI 是一个命令行工具，用于在工作目录中直接处理需求内容描述并生成代码。

## 安装

### 自动安装

```bash
# 进入cli目录
cd /path/to/numa_avatar/mvp/cli

# 安装qwen命令
python install.py
```

### 手动安装

```bash
# 复制qwen.py到系统PATH中的目录
cp qwen.py ~/bin/qwen
chmod +x ~/bin/qwen
```

## 使用方法

### 基本用法

```bash
# 进入工作目录
cd working_directory

# 使用qwen处理需求
qwen -p "创建一个Python Flask应用，包含一个返回'Hello, World!'的路由"
```

### 命令行参数

```bash
qwen -h  # 显示帮助信息

# 指定需求内容
qwen "创建一个简单的Web应用"
qwen -p "创建一个简单的Web应用"

# 指定工作目录
qwen -p "创建一个简单的Web应用" -d /path/to/project

# 指定模型和温度参数
qwen -p "创建一个简单的Web应用" -m gpt-3.5-turbo -t 0.8

# 详细输出
qwen -p "创建一个简单的Web应用" -v
```

## 配置

Qwen CLI 会按以下顺序查找API密钥：

1. 环境变量 `OPENAI_API_KEY`
2. 配置文件 `config.yaml` 中的 `llm.api_key`
3. 交互式输入

## 与Avatar的区别

| 特性 | Qwen CLI | Avatar |
|------|----------|--------|
| 运行方式 | 手动执行 | 持续运行，监听任务 |
| API集成 | 直接调用LLM API | 通过后端API通信 |
| 任务来源 | 命令行参数 | 后端消息订阅 |
| Git操作 | 无 | 完整的Git操作 |
| 日志记录 | 基本日志 | 详细任务日志 |
| 工作区管理 | 当前目录 | 专用工作区 |

## 示例

```bash
# 进入项目目录
cd my_project

# 生成一个简单的Web应用
qwen -p "创建一个Python Flask应用，包含一个返回'Hello, World!'的路由"

# 生成一个React组件
qwen -p "创建一个React组件，显示用户列表，每个用户有姓名和邮箱"
```