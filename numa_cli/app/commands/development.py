import click
import json
from app.core.http_client import client

@click.group()
def development():
    """开发管理相关命令"""
    pass

@development.command()
@click.option('--title', prompt='开发任务标题', help='开发任务标题')
@click.option('--description', prompt='开发任务描述', help='开发任务详细描述')
@click.option('--solution-id', type=int, prompt='方案ID', help='关联的方案ID')
@click.option('--assigned-to', type=int, prompt='分配给用户ID', help='分配给的用户ID')
def create(title, description, solution_id, assigned_to):
    """创建新开发任务"""
    payload = {
        "title": title,
        "description": description,
        "solution_id": solution_id,
        "assigned_to": assigned_to
    }
    
    try:
        response = client.post("/v1/development/", json=payload)
        if response.status_code == 200:
            click.echo(f"成功创建开发任务: {response.json()}")
        else:
            click.echo(f"创建开发任务失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@development.command()
@click.argument('task_id', type=int)
def get(task_id):
    """获取指定ID的开发任务"""
    try:
        response = client.get(f"/v1/development/{task_id}")
        if response.status_code == 200:
            task = response.json()
            click.echo(json.dumps(task, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取开发任务失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@development.command()
@click.option('--skip', default=0, help='跳过的记录数')
@click.option('--limit', default=100, help='返回的记录数')
def list(skip, limit):
    """获取开发任务列表"""
    try:
        response = client.get("/v1/development/", params={"skip": skip, "limit": limit})
        if response.status_code == 200:
            tasks = response.json()
            click.echo(json.dumps(tasks, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取开发任务列表失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

if __name__ == '__main__':
    development()