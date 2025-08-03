import click
import json
from app.core.http_client import client

@click.group()
def solutions():
    """方案管理相关命令"""
    pass

@solutions.command()
@click.option('--title', prompt='方案标题', help='方案标题')
@click.option('--description', prompt='方案描述', help='方案详细描述')
@click.option('--requirement-id', type=int, prompt='需求ID', help='关联的需求ID')
def create(title, description, requirement_id):
    """创建新方案"""
    payload = {
        "title": title,
        "description": description,
        "requirement_id": requirement_id
    }
    
    try:
        response = client.post("/v1/solutions/", json=payload)
        if response.status_code == 200:
            click.echo(f"成功创建方案: {response.json()}")
        else:
            click.echo(f"创建方案失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@solutions.command()
@click.argument('solution_id', type=int)
def get(solution_id):
    """获取指定ID的方案"""
    try:
        response = client.get(f"/v1/solutions/{solution_id}")
        if response.status_code == 200:
            solution = response.json()
            click.echo(json.dumps(solution, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取方案失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@solutions.command()
@click.option('--skip', default=0, help='跳过的记录数')
@click.option('--limit', default=100, help='返回的记录数')
def list(skip, limit):
    """获取方案列表"""
    try:
        response = client.get("/v1/solutions/", params={"skip": skip, "limit": limit})
        if response.status_code == 200:
            solutions = response.json()
            click.echo(json.dumps(solutions, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取方案列表失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

if __name__ == '__main__':
    solutions()