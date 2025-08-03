"""添加需求clarified字段

Revision ID: 002_add_requirements_clarified
Revises: 001_initial_schema
Create Date: 2025-08-03 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = '002_add_requirements_clarified'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade():
    # 检查clarified字段是否已存在
    conn = op.get_bind()
    result = conn.execute(text("PRAGMA table_info(requirements)")).fetchall()
    columns = [row[1] for row in result]  # 获取所有列名
    
    # 如果clarified字段不存在，则添加它
    if 'clarified' not in columns:
        op.add_column('requirements', sa.Column('clarified', sa.Boolean(), nullable=True))
        op.execute("UPDATE requirements SET clarified = 0")  # 默认设置为False


def downgrade():
    # 删除clarified字段
    op.drop_column('requirements', 'clarified')