"""empty message

Revision ID: daa0f4151d84
Revises: 62029f7f7106
Create Date: 2024-10-31 15:31:41.031997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'daa0f4151d84'
down_revision = '62029f7f7106'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starship', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable='False')
        batch_op.alter_column('model',
               existing_type=sa.VARCHAR(),
               nullable='False')
        batch_op.alter_column('manufacturer',
               existing_type=sa.VARCHAR(),
               nullable='False')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('starship', schema=None) as batch_op:
        batch_op.alter_column('manufacturer',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('model',
               existing_type=sa.VARCHAR(),
               nullable=True)
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###