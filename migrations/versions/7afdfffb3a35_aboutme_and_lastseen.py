"""aboutme and lastseen

Revision ID: 7afdfffb3a35
Revises: 66e24882278d
Create Date: 2020-04-23 11:59:00.993681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7afdfffb3a35'
down_revision = '66e24882278d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###
