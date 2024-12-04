"""Initial

Revision ID: c06bd7bda2b7
Revises: 
Create Date: 2024-12-04 17:01:53.543948

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c06bd7bda2b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('attachment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('file_url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('icon', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('middle_name', sa.String(length=50), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.Column('phone', sa.String(length=15), nullable=False),
    sa.Column('is_admin', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('is_verified', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('has_children', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('profile_photo', sa.String(), nullable=True),
    sa.Column('work_start_date', sa.Date(), nullable=True),
    sa.Column('work_end_date', sa.Date(), nullable=True),
    sa.Column('legal_entity', sa.String(length=128), nullable=True),
    sa.Column('position', sa.String(length=50), nullable=True),
    sa.Column('department', sa.String(length=50), nullable=True),
    sa.Column('balance', sa.Integer(), server_default='2000', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP)"), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('benefit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=256), nullable=False),
    sa.Column('provider', sa.String(length=256), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=False),
    sa.Column('picture', sa.String(), nullable=True),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('required_experience', sa.String(length=25), nullable=True),
    sa.Column('childs_required', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default='true', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP)"), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('token',
    sa.Column('jti', sa.String(length=255), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('revoked', sa.Boolean(), server_default='false', nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('jti')
    )
    op.create_table('benefit_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('benefit_id', sa.Integer(), nullable=False),
    sa.Column('instructions', sa.String(length=2000), nullable=True),
    sa.Column('period', sa.String(length=25), nullable=True),
    sa.Column('is_cancellable', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['benefit_id'], ['benefit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('benefit_id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('benefit_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(length=2000), nullable=False),
    sa.Column('required_experience', sa.String(length=25), nullable=True),
    sa.ForeignKeyConstraint(['benefit_id'], ['benefit.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), server_default='in_work', nullable=False),
    sa.Column('benefit_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('option_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('activated_at', sa.DateTime(), nullable=True),
    sa.Column('ends_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['benefit_id'], ['benefit.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['option_id'], ['option.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=2000), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('attachment_id', sa.Integer(), nullable=True),
    sa.Column('is_read', sa.Boolean(), server_default='false', nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP)"), nullable=False),
    sa.ForeignKeyConstraint(['attachment_id'], ['attachment.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('order')
    op.drop_table('option')
    op.drop_table('benefit_content')
    op.drop_table('token')
    op.drop_table('benefit')
    op.drop_table('users')
    op.drop_table('category')
    op.drop_table('attachment')
    # ### end Alembic commands ###
