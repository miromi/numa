import click
import requests

# API基础URL
API_BASE_URL = "http://localhost:7301/api/v1"

def get_users_api():
    """通过API获取用户列表"""
    url = f"{API_BASE_URL}/users/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@click.group()
def users():
    """用户管理命令"""
    pass

@users.command()
def list():
    """列出所有用户"""
    try:
        users = get_users_api()
        if users:
            click.echo("用户列表:")
            for user in users:
                click.echo(f"  ID: {user['id']}, 姓名: {user['name']}, 邮箱: {user['email']}")
        else:
            click.echo("暂无用户")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取用户列表失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取用户列表失败: {str(e)}")