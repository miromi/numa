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
@click.option('--created-by', type=int, prompt='创建人ID', help='方案创建人ID')
def create(title, description, requirement_id, created_by):
    """创建新方案"""
    payload = {
        "title": title,
        "description": description,
        "requirement_id": requirement_id,
        "created_by": created_by
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

@solutions.command()
@click.argument('solution_id', type=int)
@click.option('--requirement-id', type=int, help='关联的需求ID')
def by_requirement(requirement_id):
    """根据需求ID获取方案列表"""
    try:
        response = client.get(f"/v1/solutions/requirement/{requirement_id}")
        if response.status_code == 200:
            solutions = response.json()
            click.echo(json.dumps(solutions, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取方案列表失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@solutions.command()
@click.argument('solution_id', type=int)
@click.option('--confirmed', is_flag=True, help='标记为已确认')
@click.option('--not-confirmed', is_flag=True, help='标记为未确认')
def confirm(solution_id, confirmed, not_confirmed):
    """确认/取消确认方案"""
    if confirmed and not_confirmed:
        click.echo("不能同时设置confirmed和not_confirmed")
        return
    
    confirmed_value = True if confirmed else (False if not_confirmed else True)
    
    try:
        response = client.patch(f"/v1/solutions/{solution_id}/confirm", params={"confirmed": confirmed_value})
        if response.status_code == 200:
            solution = response.json()
            status = "已确认" if confirmed_value else "未确认"
            click.echo(f"成功{status}方案: {json.dumps(solution, indent=2, ensure_ascii=False)}")
        else:
            click.echo(f"确认方案失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

# 方案问题相关命令
@solutions.group()
def questions():
    """方案问题管理相关命令"""
    pass

@questions.command()
@click.option('--content', prompt='问题内容', help='问题内容')
@click.option('--solution-id', type=int, prompt='方案ID', help='关联的方案ID')
@click.option('--created-by', type=int, prompt='提问人ID', help='提问人ID')
def create_question(content, solution_id, created_by):
    """创建新问题"""
    payload = {
        "content": content,
        "solution_id": solution_id,
        "created_by": created_by
    }
    
    try:
        response = client.post("/v1/solutions/questions/", json=payload, params={"current_user_id": created_by})
        if response.status_code == 200:
            click.echo(f"成功创建问题: {response.json()}")
        else:
            click.echo(f"创建问题失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@questions.command()
@click.argument('question_id', type=int)
def get_question(question_id):
    """获取指定ID的问题"""
    try:
        response = client.get(f"/v1/solutions/questions/{question_id}")
        if response.status_code == 200:
            question = response.json()
            click.echo(json.dumps(question, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取问题失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@questions.command()
@click.argument('solution_id', type=int)
def list_questions(solution_id):
    """获取指定方案的问题列表"""
    try:
        response = client.get(f"/v1/solutions/questions/solution/{solution_id}")
        if response.status_code == 200:
            questions = response.json()
            click.echo(json.dumps(questions, indent=2, ensure_ascii=False))
        else:
            click.echo(f"获取问题列表失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@questions.command()
@click.argument('question_id', type=int)
@click.option('--answer', prompt='回答内容', help='回答内容')
@click.option('--answered-by', type=int, prompt='回答人ID', help='回答人ID')
def answer_question(question_id, answer, answered_by):
    """回答问题"""
    try:
        response = client.patch(
            f"/v1/solutions/questions/{question_id}/answer",
            params={
                "answer": answer,
                "answered_by": answered_by,
                "current_user_id": answered_by
            }
        )
        if response.status_code == 200:
            question = response.json()
            click.echo(f"成功回答问题: {json.dumps(question, indent=2, ensure_ascii=False)}")
        else:
            click.echo(f"回答问题失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

@questions.command()
@click.argument('question_id', type=int)
@click.option('--clarified-by', type=int, prompt='澄清人ID', help='澄清人ID（必须是方案负责人）')
def clarify_question(question_id, clarified_by):
    """标记问题为已澄清"""
    try:
        response = client.patch(
            f"/v1/solutions/questions/{question_id}/clarify",
            params={
                "clarified_by": clarified_by,
                "current_user_id": clarified_by
            }
        )
        if response.status_code == 200:
            question = response.json()
            click.echo(f"成功标记问题为已澄清: {json.dumps(question, indent=2, ensure_ascii=False)}")
        else:
            click.echo(f"标记问题失败: {response.text}")
    except Exception as e:
        click.echo(f"发生错误: {str(e)}")

if __name__ == '__main__':
    solutions()