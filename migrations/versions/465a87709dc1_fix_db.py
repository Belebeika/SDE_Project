"""fix db

Revision ID: 465a87709dc1
Revises: f26a192b6413
Create Date: 2024-01-17 12:47:16.314475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '465a87709dc1'
down_revision = 'f26a192b6413'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('job_attachment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_attachment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('filename', sa.VARCHAR(length=300), nullable=False),
    sa.Column('job_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###