"""empty message

Revision ID: 1850ff4bf7a0
Revises: 
Create Date: 2025-01-29 20:05:02.532203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1850ff4bf7a0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planets',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('gravity', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_planets_uid'), ['uid'], unique=True)

    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_id'), ['id'], unique=False)

    op.create_table('favorites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('external_id', sa.Integer(), nullable=False),
    sa.Column('type', sa.Enum('SPECIES', 'PLANETS', 'PEOPLE', name='favoritestype'), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_favorites_id'), ['id'], unique=False)
        batch_op.create_index(batch_op.f('ix_favorites_user_id'), ['user_id'], unique=False)

    op.create_table('people',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('homeworld', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['homeworld'], ['planets.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_people_uid'), ['uid'], unique=True)

    op.create_table('species',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('homeworld', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['homeworld'], ['planets.uid'], ),
    sa.PrimaryKeyConstraint('uid')
    )
    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_species_uid'), ['uid'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('species', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_species_uid'))

    op.drop_table('species')
    with op.batch_alter_table('people', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_people_uid'))

    op.drop_table('people')
    with op.batch_alter_table('favorites', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_favorites_user_id'))
        batch_op.drop_index(batch_op.f('ix_favorites_id'))

    op.drop_table('favorites')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_id'))

    op.drop_table('user')
    with op.batch_alter_table('planets', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_planets_uid'))

    op.drop_table('planets')
    # ### end Alembic commands ###
