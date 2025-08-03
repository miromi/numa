import click
import json
from app.core.http_client import client

@click.group()
def requirements():
    """需求管理相关命令"""
    pass

@requirements.command()
@click.option('--title', prompt='需求标题', help='需求标题')
@click.option('--description', prompt='需求描述', help='需求详细描述')
@click.option('--user-id', type=int, prompt='用户ID', help='关联的用户ID')
def create(title, description, user_id):
    """创建新需求"""
    payload = {
        "title": title,
        "description": description,
        "user_id": user_id
    }
    
    try:
        response = client.post("/v1/requirements/", json=payload)
        if response.status_code == 200:
            click.echo(f"成功创建需求: {response.json()}")
        else:
            click.echo(f"创建需求失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@requirements.command()
@click.argument('requirement_id', type=int)
def get(requirement_id):
    """获取指定ID的需求"""
    try:
        response = client.get(f"/v1/requirements/{requirement_id}")
        if response.status_code == 200:
            requirement = response.json()
            click.echo(json.dumps(requirement, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取需求失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@requirements.command()
@click.option('--skip', default=0, help='跳过的记录数')
@click.option('--limit', default=100, help='返回的记录数')
def list(skip, limit):
    """获取需求列表"""
    try:
        response = client.get("/v1/requirements/", params={"skip": skip, "limit": limit})
        if response.status_code == 200:
            requirements = response.json()
            click.echo(json.dumps(requirements, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取需求列表失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

if __name__ == '__main__':
    requirements()