import click
import json
from app.core.http_client import client

@click.group()
def deployment():
    """部署管理相关命令"""
    pass

@deployment.command()
@click.option('--name', prompt='部署名称', help='部署名称')
@click.option('--description', prompt='部署描述', help='部署详细描述')
@click.option('--development-task-id', type=int, prompt='开发任务ID', help='关联的开发任务ID')
@click.option('--deployed-by', type=int, prompt='部署者用户ID', help='执行部署的用户ID')
def create(name, description, development_task_id, deployed_by):
    """创建新部署记录"""
    payload = {
        "name": name,
        "description": description,
        "development_task_id": development_task_id,
        "deployed_by": deployed_by
    }
    
    try:
        response = client.post("/v1/deployment/", json=payload)
        if response.status_code == 200:
            click.echo(f"成功创建部署记录: {response.json()}")
        else:
            click.echo(f"创建部署记录失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@deployment.command()
@click.argument('deployment_id', type=int)
def get(deployment_id):
    """获取指定ID的部署记录"""
    try:
        response = client.get(f"/v1/deployment/{deployment_id}")
        if response.status_code == 200:
            deployment = response.json()
            click.echo(json.dumps(deployment, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取部署记录失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@deployment.command()
@click.option('--skip', default=0, help='跳过的记录数')
@click.option('--limit', default=100, help='返回的记录数')
def list(skip, limit):
    """获取部署记录列表"""
    try:
        response = client.get("/v1/deployment/", params={"skip": skip, "limit": limit})
        if response.status_code == 200:
            deployments = response.json()
            click.echo(json.dumps(deployments, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取部署记录列表失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

if __name__ == '__main__':
    deployment()