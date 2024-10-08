"""added trucks and trailers tables

Revision ID: 26e1670bc7f2
Revises: b269eccea7bb
Create Date: 2024-09-22 19:31:59.744926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26e1670bc7f2'
down_revision = 'b269eccea7bb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('trucks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('truck_number', sa.String(length=9), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('trucks', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_trucks_truck_number'), ['truck_number'], unique=True)

    op.create_table('trailers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('trailer_number', sa.String(length=9), nullable=False),
    sa.Column('truck_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['truck_id'], ['trucks.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('trailers', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_trailers_trailer_number'), ['trailer_number'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('trailers', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_trailers_trailer_number'))

    op.drop_table('trailers')
    with op.batch_alter_table('trucks', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_trucks_truck_number'))

    op.drop_table('trucks')
    # ### end Alembic commands ###
