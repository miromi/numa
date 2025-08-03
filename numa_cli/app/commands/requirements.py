import click
import requests

# API基础URL
API_BASE_URL = "http://localhost:8000/api/v1"

def create_requirement_api(title, description, user_id, application_id=None):
    """通过API创建需求"""
    url = f"{API_BASE_URL}/requirements/"
    data = {
        "title": title,
        "description": description,
        "user_id": user_id
    }
    
    if application_id is not None:
        data["application_id"] = application_id
    
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()

def get_requirement_api(requirement_id):
    """通过API获取需求详情"""
    url = f"{API_BASE_URL}/requirements/{requirement_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def list_requirements_api():
    """通过API列出所有需求"""
    url = f"{API_BASE_URL}/requirements/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def assign_requirement_api(requirement_id, assigned_to):
    """通过API分配需求"""
    url = f"{API_BASE_URL}/requirements/{requirement_id}/assign"
    params = {"assigned_to": assigned_to}
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()

def confirm_requirement_api(requirement_id):
    """通过API确认需求"""
    url = f"{API_BASE_URL}/requirements/{requirement_id}/confirm"
    response = requests.post(url)
    response.raise_for_status()
    return response.json()

@click.group()
def requirements():
    """需求管理命令"""
    pass

@requirements.command()
@click.option('--title', required=True, help='需求标题')
@click.option('--description', required=True, help='需求描述')
@click.option('--user-id', required=True, type=int, help='用户ID')
@click.option('--application-id', type=int, help='关联的应用ID（可选）')
def create(title, description, user_id, application_id):
    """创建新需求"""
    try:
        requirement = create_requirement_api(title, description, user_id, application_id)
        click.echo(f"成功创建需求: {requirement}")
    except requests.exceptions.RequestException as e:
        click.echo(f"创建需求失败: {str(e)}")
    except Exception as e:
        click.echo(f"创建需求失败: {str(e)}")

@requirements.command()
@click.argument('requirement_id', type=int)
def get(requirement_id):
    """获取需求详情"""
    try:
        requirement = get_requirement_api(requirement_id)
        click.echo(f"需求详情: {requirement}")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取需求详情失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取需求详情失败: {str(e)}")

@requirements.command()
def list():
    """列出所有需求"""
    try:
        requirements = list_requirements_api()
        if requirements:
            for req in requirements:
                click.echo(f"ID: {req['id']}, 标题: {req['title']}, 状态: {req['status']}")
        else:
            click.echo("暂无需求")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取需求列表失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取需求列表失败: {str(e)}")

@requirements.command()
@click.argument('requirement_id', type=int)
@click.option('--assigned-to', required=True, type=int, help='接手人用户ID')
def assign(requirement_id, assigned_to):
    """分配需求给指定用户"""
    try:
        requirement = assign_requirement_api(requirement_id, assigned_to)
        click.echo(f"成功分配需求给用户 {assigned_to}")
        click.echo(f"分支名称: {requirement.get('branch_name')}")
        click.echo(f"规范文档: {requirement.get('spec_document')}")
    except requests.exceptions.RequestException as e:
        click.echo(f"分配需求失败: {str(e)}")
    except Exception as e:
        click.echo(f"分配需求失败: {str(e)}")

@requirements.command()
@click.argument('requirement_id', type=int)
def confirm(requirement_id):
    """确认需求澄清完毕"""
    try:
        requirement = confirm_requirement_api(requirement_id)
        click.echo(f"成功确认需求 {requirement_id}，状态更新为: {requirement['status']}")
    except requests.exceptions.RequestException as e:
        click.echo(f"确认需求失败: {str(e)}")
    except Exception as e:
        click.echo(f"确认需求失败: {str(e)}")