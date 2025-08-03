"""添加方案和方案问题表

Revision ID: 003_add_solutions_and_questions
Revises: 002_add_requirements_clarified
Create Date: 2025-08-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '003_add_solutions_and_questions'
down_revision = '002_add_requirements_clarified'
branch_labels = None
depends_on = None


def upgrade():
    # 获取数据库连接
    conn = op.get_bind()
    
    # 检查solutions表是否已存在
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='solutions'")).fetchone()
    
    # 如果solutions表不存在，则创建它
    if not result:
        op.create_table('solutions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('title', sa.String(), nullable=True),
            sa.Column('description', sa.Text(), nullable=True),
            sa.Column('requirement_id', sa.Integer(), nullable=True),
            sa.Column('status', sa.String(), nullable=True),
            sa.Column('created_by', sa.Integer(), nullable=True),
            sa.Column('clarified', sa.Boolean(), nullable=True),
            sa.ForeignKeyConstraint(['requirement_id'], ['requirements.id'], ),
            sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_solutions_title'), 'solutions', ['title'], unique=False)
    else:
        # 如果表已存在，检查并添加缺失的列
        columns = conn.execute(text("PRAGMA table_info(solutions)")).fetchall()
        column_names = [col[1] for col in columns]
        
        if 'created_by' not in column_names:
            op.execute("ALTER TABLE solutions ADD COLUMN created_by INTEGER")
            
        if 'clarified' not in column_names:
            op.execute("ALTER TABLE solutions ADD COLUMN clarified BOOLEAN")
    
    # 检查solution_questions表是否已存在
    result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='solution_questions'")).fetchone()
    
    # 如果solution_questions表不存在，则创建它
    if not result:
        op.create_table('solution_questions',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('solution_id', sa.Integer(), nullable=False),
            sa.Column('created_by', sa.Integer(), nullable=False),
            sa.Column('answered_by', sa.Integer(), nullable=True),
            sa.Column('answer', sa.Text(), nullable=True),
            sa.Column('clarified', sa.Boolean(), nullable=True),
            sa.Column('clarified_by', sa.Integer(), nullable=True),
            sa.ForeignKeyConstraint(['solution_id'], ['solutions.id'], ),
            sa.ForeignKeyConstraint(['created_by'], ['users.id'], ),
            sa.ForeignKeyConstraint(['answered_by'], ['users.id'], ),
            sa.ForeignKeyConstraint(['clarified_by'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )


def downgrade():
    # 删除方案问题表
    op.drop_table('solution_questions')
    
    # 删除方案表
    op.drop_index(op.f('ix_solutions_title'), table_name='solutions')
    op.drop_table('solutions')