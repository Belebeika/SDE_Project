"""Initial migration

Revision ID: a677b43bb1fe
Revises: 84aa6fb895bb
Create Date: 2023-12-09 03:04:14.239882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a677b43bb1fe'
down_revision = '84aa6fb895bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('requirements', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=300), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('skills', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('rezume_images')
    op.drop_table('rezume')
    op.drop_table('vacancy_images')
    op.drop_table('vacancy')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('vacancy',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.Column('text', sa.VARCHAR(), nullable=False),
    sa.Column('title_image', sa.BLOB(), nullable=False),
    sa.Column('User_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['User_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancy_images',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('image', sa.BLOB(), nullable=False),
    sa.Column('Vacancy_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['Vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rezume',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(), nullable=False),
    sa.Column('text', sa.VARCHAR(), nullable=False),
    sa.Column('title_image', sa.BLOB(), nullable=False),
    sa.Column('User_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['User_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rezume_images',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('image', sa.BLOB(), nullable=False),
    sa.Column('Rezume_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['Rezume_id'], ['rezume.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('resume')
    op.drop_table('job')
    # ### end Alembic commands ###