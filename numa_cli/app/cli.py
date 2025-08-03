import click
from app.commands.requirements import requirements
from app.commands.solutions import solutions
from app.commands.development import development
from app.commands.deployment import deployment
from app.commands.users import users

@click.group()
def cli():
    """Numa CLI - 自动化DevOps流程工具"""
    pass

# 添加各个模块的命令组
cli.add_command(requirements)
cli.add_command(solutions)
cli.add_command(development)
cli.add_command(deployment)
cli.add_command(users)

if __name__ == '__main__':
    cli()