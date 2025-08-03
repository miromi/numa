import click
import json
from app.core.http_client import client

@click.group()
def users():
    """用户管理相关命令"""
    pass

@users.command()
@click.option('--name', prompt='用户姓名', help='用户姓名')
@click.option('--email', prompt='用户邮箱', help='用户邮箱地址')
def create(name, email):
    """创建新用户"""
    payload = {
        "name": name,
        "email": email
    }
    
    try:
        response = client.post("/v1/users/", json=payload)
        if response.status_code == 200:
            click.echo(f"成功创建用户: {response.json()}")
        else:
            click.echo(f"创建用户失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@users.command()
@click.argument('user_id', type=int)
def get(user_id):
    """获取指定ID的用户"""
    try:
        response = client.get(f"/v1/users/{user_id}")
        if response.status_code == 200:
            user = response.json()
            click.echo(json.dumps(user, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取用户失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@users.command()
@click.option('--skip', default=0, help='跳过的记录数')
@click.option('--limit', default=100, help='返回的记录数')
def list(skip, limit):
    """获取用户列表"""
    try:
        response = client.get("/v1/users/", params={"skip": skip, "limit": limit})
        if response.status_code == 200:
            users = response.json()
            click.echo(json.dumps(users, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取用户列表失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

if __name__ == '__main__':
    users()