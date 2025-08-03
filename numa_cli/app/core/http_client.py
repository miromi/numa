import httpx

# 创建全局HTTP客户端
client = httpx.Client(base_url="http://localhost:8000/api")