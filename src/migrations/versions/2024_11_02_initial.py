"""Initial

Revision ID: bf08202d3092
Revises: 
Create Date: 2024-11-02 19:07:08.536758

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf08202d3092'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
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
    sa.Column('work_start_date', sa.Date(), nullable=True),
    sa.Column('work_end_date', sa.Date(), nullable=True),
    sa.Column('position', sa.String(length=50), nullable=True),
    sa.Column('department', sa.String(length=50), nullable=True),
    sa.Column('coins', sa.Integer(), server_default='2000', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('benefit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('period', sa.String(length=25), nullable=True),
    sa.Column('instructions', sa.String(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('is_cancellable', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.Date(), server_default=sa.text("DATE(TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP))"), nullable=False),
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
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), server_default='in_work', nullable=False),
    sa.Column('benefit_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP)"), nullable=False),
    sa.Column('activated_at', sa.DateTime(), nullable=True),
    sa.Column('ends_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['benefit_id'], ['benefit.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.String(length=256), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('Asia/Yekaterinburg', CURRENT_TIMESTAMP)"), nullable=False),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('order')
    op.drop_table('token')
    op.drop_table('benefit')
    op.drop_table('users')
    op.drop_table('category')
    # ### end Alembic commands ###
