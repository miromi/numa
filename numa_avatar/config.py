import yaml
import os

class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self):
        """加载配置文件"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        else:
            # 返回默认配置
            return {
                "backend": {
                    "url": "http://localhost:7301",
                    "api_token": ""
                },
                "git": {
                    "username": "",
                    "email": ""
                },
                "avatar": {
                    "id": "avatar_001",
                    "name": "Developer Avatar"
                },
                "polling": {
                    "interval": 5
                }
            }
    
    def get(self, key_path: str, default=None):
        """获取配置项
        
        Args:
            key_path: 配置项路径，如 "backend.url"
            default: 默认值
        """
        keys = key_path.split('.')
        value = self.config
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value):
        """设置配置项
        
        Args:
            key_path: 配置项路径，如 "backend.url"
            value: 配置值
        """
        keys = key_path.split('.')
        config = self.config
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        config[keys[-1]] = value
        
        # 保存到文件
        with open(self.config_path, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)