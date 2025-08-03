import os

# API基础URL
API_BASE_URL = os.getenv("NUMA_API_URL", "http://localhost:8000/api")

# 默认分页参数
DEFAULT_LIMIT = 100
DEFAULT_SKIP = 0