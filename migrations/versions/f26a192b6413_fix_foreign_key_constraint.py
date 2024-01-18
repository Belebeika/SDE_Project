"""Fix foreign key constraint

Revision ID: f26a192b6413
Revises: 454a5bd99756
Create Date: 2024-01-17 12:34:34.971046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f26a192b6413'
down_revision = '454a5bd99756'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.add_column(sa.Column('resume_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_job_resume_id', 'resume', ['resume_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job', schema=None) as batch_op:
        batch_op.drop_constraint('fk_job_resume_id', type_='foreignkey')
        batch_op.drop_column('resume_id')

    # ### end Alembic commands ###