import click
import requests

# API基础URL
API_BASE_URL = "http://localhost:8000/api/v1"

def create_application_api(name, description, development_task_id, created_by, repository_url, owner, app_id):
    """通过API创建应用"""
    url = f"{API_BASE_URL}/applications/"
    data = {
        "name": name,
        "description": description,
        "development_task_id": development_task_id,
        "created_by": created_by,
        "repository_url": repository_url,
        "owner": owner,
        "app_id": app_id
    }
    response = requests.post(url, json=data)
    response.raise_for_status()
    return response.json()

def get_application_api(application_id):
    """通过API获取应用详情"""
    url = f"{API_BASE_URL}/applications/{application_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_application_by_app_id_api(app_id):
    """通过API根据app_id获取应用详情"""
    url = f"{API_BASE_URL}/applications/by_app_id/{app_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def list_applications_api():
    """通过API列出所有应用"""
    url = f"{API_BASE_URL}/applications/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

@click.group()
def applications():
    """应用管理命令"""
    pass

@applications.command()
@click.option('--name', required=True, help='应用名称')
@click.option('--description', required=True, help='应用描述')
@click.option('--development-task-id', required=True, type=int, help='关联的开发任务ID')
@click.option('--created-by', required=True, type=int, help='创建者ID')
@click.option('--repository-url', required=True, help='Git仓库地址')
@click.option('--owner', required=True, help='应用所有者')
@click.option('--app-id', required=True, help='应用ID')
def create(name, description, development_task_id, created_by, repository_url, owner, app_id):
    """创建新应用"""
    try:
        application = create_application_api(name, description, development_task_id, created_by, repository_url, owner, app_id)
        click.echo(f"应用创建成功，ID: {application['id']}")
        click.echo(f"名称: {application['name']}")
        click.echo(f"描述: {application['description']}")
        click.echo(f"状态: {application['status']}")
        click.echo(f"仓库地址: {application['repository_url']}")
        click.echo(f"所有者: {application['owner']}")
        click.echo(f"应用ID: {application['app_id']}")
    except requests.exceptions.RequestException as e:
        click.echo(f"创建应用失败: {str(e)}")
    except Exception as e:
        click.echo(f"创建应用失败: {str(e)}")

@applications.command()
@click.argument('application_id', type=int)
def get(application_id):
    """获取应用详情"""
    try:
        application = get_application_api(application_id)
        click.echo(f"ID: {application['id']}")
        click.echo(f"名称: {application['name']}")
        click.echo(f"描述: {application['description']}")
        click.echo(f"状态: {application['status']}")
        click.echo(f"开发任务ID: {application['development_task_id']}")
        click.echo(f"创建者ID: {application['created_by']}")
        click.echo(f"仓库地址: {application['repository_url']}")
        click.echo(f"所有者: {application['owner']}")
        click.echo(f"应用ID: {application['app_id']}")
        click.echo(f"创建时间: {application['created_at']}")
        if application.get('built_at'):
            click.echo(f"构建时间: {application['built_at']}")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取应用详情失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取应用详情失败: {str(e)}")

@applications.command()
@click.argument('app_id')
def get_by_app_id(app_id):
    """根据应用ID获取应用详情"""
    try:
        application = get_application_by_app_id_api(app_id)
        click.echo(f"ID: {application['id']}")
        click.echo(f"名称: {application['name']}")
        click.echo(f"描述: {application['description']}")
        click.echo(f"状态: {application['status']}")
        click.echo(f"开发任务ID: {application['development_task_id']}")
        click.echo(f"创建者ID: {application['created_by']}")
        click.echo(f"仓库地址: {application['repository_url']}")
        click.echo(f"所有者: {application['owner']}")
        click.echo(f"应用ID: {application['app_id']}")
        click.echo(f"创建时间: {application['created_at']}")
        if application.get('built_at'):
            click.echo(f"构建时间: {application['built_at']}")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取应用详情失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取应用详情失败: {str(e)}")

@applications.command()
def list():
    """列出所有应用"""
    try:
        applications = list_applications_api()
        if applications:
            for app in applications:
                click.echo(f"ID: {app['id']}, 名称: {app['name']}, 状态: {app['status']}, 应用ID: {app['app_id']}")
        else:
            click.echo("暂无应用")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取应用列表失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取应用列表失败: {str(e)}")