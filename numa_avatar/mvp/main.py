import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from avatar import Avatar

def main():
    """主函数"""
    avatar = Avatar()
    avatar.start()

if __name__ == "__main__":
    main()