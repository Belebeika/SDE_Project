"""first_init

Revision ID: 84aa6fb895bb
Revises: 
Create Date: 2023-12-03 17:57:30.116712

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '84aa6fb895bb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('firstname', sa.String(length=80), nullable=False),
    sa.Column('lastname', sa.String(length=80), nullable=False),
    sa.Column('region', sa.String(length=30), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rezume',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('title_image', sa.LargeBinary(), nullable=False),
    sa.Column('User_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['User_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancy',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('title_image', sa.LargeBinary(), nullable=False),
    sa.Column('User_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['User_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rezume_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=False),
    sa.Column('Rezume_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['Rezume_id'], ['rezume.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vacancy_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.LargeBinary(), nullable=False),
    sa.Column('Vacancy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['Vacancy_id'], ['vacancy.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('vacancy_images')
    op.drop_table('rezume_images')
    op.drop_table('vacancy')
    op.drop_table('rezume')
    op.drop_table('user')
    # ### end Alembic commands ###