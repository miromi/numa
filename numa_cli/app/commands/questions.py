import click
import requests

# API基础URL
API_BASE_URL = "http://localhost:7301/api/v1"

def create_question_api(content, requirement_id, created_by):
    """通过API创建问题"""
    url = f"{API_BASE_URL}/questions/"
    data = {
        "content": content,
        "requirement_id": requirement_id,
        "created_by": created_by
    }
    params = {"current_user_id": created_by}
    response = requests.post(url, json=data, params=params)
    response.raise_for_status()
    return response.json()

def get_question_api(question_id):
    """通过API获取问题详情"""
    url = f"{API_BASE_URL}/questions/{question_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def list_questions_by_requirement_api(requirement_id):
    """通过API列出需求的所有问题"""
    url = f"{API_BASE_URL}/questions/requirement/{requirement_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def answer_question_api(question_id, answer, answered_by):
    """通过API回答问题"""
    url = f"{API_BASE_URL}/questions/{question_id}/answer"
    params = {
        "answer": answer,
        "answered_by": answered_by,
        "current_user_id": answered_by
    }
    response = requests.patch(url, params=params)
    response.raise_for_status()
    return response.json()

def clarify_question_api(question_id, clarified_by):
    """通过API标记问题为已澄清"""
    url = f"{API_BASE_URL}/questions/{question_id}/clarify"
    params = {
        "clarified_by": clarified_by,
        "current_user_id": clarified_by
    }
    response = requests.patch(url, params=params)
    response.raise_for_status()
    return response.json()

@click.group()
def questions():
    """问题管理命令"""
    pass

@questions.command()
@click.option('--content', required=True, help='问题内容')
@click.option('--requirement-id', required=True, type=int, help='需求ID')
@click.option('--created-by', required=True, type=int, help='提问人ID')
def create(content, requirement_id, created_by):
    """创建新问题"""
    try:
        question = create_question_api(content, requirement_id, created_by)
        click.echo(f"成功创建问题: {question}")
    except requests.exceptions.RequestException as e:
        click.echo(f"创建问题失败: {str(e)}")
    except Exception as e:
        click.echo(f"创建问题失败: {str(e)}")

@questions.command()
@click.argument('question_id', type=int)
def get(question_id):
    """获取问题详情"""
    try:
        question = get_question_api(question_id)
        click.echo(f"问题详情: {question}")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取问题详情失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取问题详情失败: {str(e)}")

@questions.command()
@click.argument('requirement_id', type=int)
def list(requirement_id):
    """列出需求的所有问题"""
    try:
        questions = list_questions_by_requirement_api(requirement_id)
        if questions:
            for q in questions:
                status = "已澄清" if q['clarified'] else "未澄清"
                click.echo(f"ID: {q['id']}, 内容: {q['content']}, 状态: {status}")
        else:
            click.echo("暂无问题")
    except requests.exceptions.RequestException as e:
        click.echo(f"获取问题列表失败: {str(e)}")
    except Exception as e:
        click.echo(f"获取问题列表失败: {str(e)}")

@questions.command()
@click.argument('question_id', type=int)
@click.option('--answer', required=True, help='回答内容')
@click.option('--answered-by', required=True, type=int, help='回答人ID')
def answer(question_id, answer, answered_by):
    """回答问题"""
    try:
        question = answer_question_api(question_id, answer, answered_by)
        click.echo(f"成功回答问题 {question_id}")
    except requests.exceptions.RequestException as e:
        click.echo(f"回答问题失败: {str(e)}")
    except Exception as e:
        click.echo(f"回答问题失败: {str(e)}")

@questions.command()
@click.argument('question_id', type=int)
@click.option('--clarified-by', required=True, type=int, help='澄清人ID（必须是需求接手人）')
def clarify(question_id, clarified_by):
    """标记问题为已澄清"""
    try:
        question = clarify_question_api(question_id, clarified_by)
        click.echo(f"成功标记问题 {question_id} 为已澄清")
    except requests.exceptions.RequestException as e:
        click.echo(f"标记问题失败: {str(e)}")
    except Exception as e:
        click.echo(f"标记问题失败: {str(e)}")