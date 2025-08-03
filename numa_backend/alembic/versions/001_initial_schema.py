"""创建初始表结构

Revision ID: 001_initial_schema
Revises: 
Create Date: 2025-08-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # 创建用户表
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建应用表
    op.create_table('applications',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('git_repo_url', sa.String(), nullable=True),
        sa.Column('owner', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建需求表
    op.create_table('requirements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('application_id', sa.Integer(), nullable=True),
        sa.Column('assigned_to', sa.Integer(), nullable=True),
        sa.Column('branch_name', sa.String(), nullable=True),
        sa.Column('spec_document', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
        sa.ForeignKeyConstraint(['assigned_to'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_requirements_title'), 'requirements', ['title'], unique=False)
    
    # 创建方案表
    op.create_table('solutions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('requirement_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['requirement_id'], ['requirements.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_solutions_title'), 'solutions', ['title'], unique=False)
    
    # 创建开发任务表
    op.create_table('development_tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('solution_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['solution_id'], ['solutions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_development_tasks_title'), 'development_tasks', ['title'], unique=False)
    
    # 创建部署表
    op.create_table('deployments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('development_task_id', sa.Integer(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['development_task_id'], ['development_tasks.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_deployments_title'), 'deployments', ['title'], unique=False)
    
    # 创建问题表
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('requirement_id', sa.Integer(), nullable=False),
        sa.Column('created_by', sa.Integer(), nullable=False),
        sa.Column('answered_by', sa.Integer(), nullable=True),
        sa.Column('answer', sa.Text(), nullable=True),
        sa.Column('clarified', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['requirement_id'], ['requirements.id'], ),
        sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
        sa.ForeignKeyConstraint(['answered_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建事件日志表
    op.create_table('event_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('event_type', sa.String(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('requirement_id', sa.Integer(), nullable=True),
        sa.Column('solution_id', sa.Integer(), nullable=True),
        sa.Column('development_task_id', sa.Integer(), nullable=True),
        sa.Column('deployment_id', sa.Integer(), nullable=True),
        sa.Column('application_id', sa.Integer(), nullable=True),
        sa.Column('question_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['requirement_id'], ['requirements.id'], ),
        sa.ForeignKeyConstraint(['solution_id'], ['solutions.id'], ),
        sa.ForeignKeyConstraint(['development_task_id'], ['development_tasks.id'], ),
        sa.ForeignKeyConstraint(['deployment_id'], ['deployments.id'], ),
        sa.ForeignKeyConstraint(['application_id'], ['applications.id'], ),
        sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # 删除所有表（按依赖关系反向删除）
    op.drop_table('event_logs')
    op.drop_table('questions')
    op.drop_index(op.f('ix_deployments_title'), table_name='deployments')
    op.drop_table('deployments')
    op.drop_index(op.f('ix_development_tasks_title'), table_name='development_tasks')
    op.drop_table('development_tasks')
    op.drop_index(op.f('ix_solutions_title'), table_name='solutions')
    op.drop_table('solutions')
    op.drop_index(op.f('ix_requirements_title'), table_name='requirements')
    op.drop_table('requirements')
    op.drop_table('applications')
    op.drop_table('users')