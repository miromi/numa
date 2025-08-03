import click
from app.commands import requirements, solutions, development, deployment, users, applications, questions

@click.group()
def cli():
    """Numa CLI工具"""
    pass

cli.add_command(requirements.requirements)
cli.add_command(solutions.solutions)
cli.add_command(development.development)
cli.add_command(deployment.deployment)
cli.add_command(users.users)
cli.add_command(applications.applications)
cli.add_command(questions.questions)

if __name__ == '__main__':
    cli()