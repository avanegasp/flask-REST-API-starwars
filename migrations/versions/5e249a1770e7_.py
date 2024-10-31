"""empty message

Revision ID: 5e249a1770e7
Revises: 0d18c76bec9c
Create Date: 2024-10-31 16:06:09.291485

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e249a1770e7'
down_revision = '0d18c76bec9c'
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