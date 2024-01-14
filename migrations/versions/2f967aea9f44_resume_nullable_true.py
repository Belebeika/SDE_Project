"""resume nullable=True

Revision ID: 2f967aea9f44
Revises: 323a834948bb
Create Date: 2024-01-12 15:24:40.967018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2f967aea9f44'
down_revision = '323a834948bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('resume', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###
