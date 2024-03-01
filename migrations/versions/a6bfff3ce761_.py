"""empty message

Revision ID: a6bfff3ce761
Revises: 3c260a06031f
Create Date: 2024-02-19 12:29:03.138268

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6bfff3ce761'
down_revision = '3c260a06031f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('email_captcha',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('captcha', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('email_captcha')
    # ### end Alembic commands ###
