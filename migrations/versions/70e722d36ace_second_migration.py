"""Second Migration

Revision ID: 70e722d36ace
Revises: e5ff6fc08d01
Create Date: 2020-06-07 04:38:17.139991

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70e722d36ace'
down_revision = 'e5ff6fc08d01'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('soundbyt_id', sa.Integer(), nullable=False))
    op.drop_constraint('comments_soundbyts_id_fkey', 'comments', type_='foreignkey')
    op.create_foreign_key(None, 'comments', 'soundbyts', ['soundbyt_id'], ['id'])
    op.drop_column('comments', 'soundbyts_id')
    op.add_column('downvotes', sa.Column('soundbyt_id', sa.Integer(), nullable=True))
    op.drop_constraint('downvotes_pitch_id_fkey', 'downvotes', type_='foreignkey')
    op.create_foreign_key(None, 'downvotes', 'soundbyts', ['soundbyt_id'], ['id'])
    op.drop_column('downvotes', 'pitch_id')
    op.add_column('soundbyts', sa.Column('soundbyt', sa.String(length=700), nullable=True))
    op.add_column('upvotes', sa.Column('soundbyt_id', sa.Integer(), nullable=True))
    op.drop_constraint('upvotes_pitch_id_fkey', 'upvotes', type_='foreignkey')
    op.create_foreign_key(None, 'upvotes', 'soundbyts', ['soundbyt_id'], ['id'])
    op.drop_column('upvotes', 'pitch_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('upvotes', sa.Column('pitch_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'upvotes', type_='foreignkey')
    op.create_foreign_key('upvotes_pitch_id_fkey', 'upvotes', 'soundbyts', ['pitch_id'], ['id'])
    op.drop_column('upvotes', 'soundbyt_id')
    op.drop_column('soundbyts', 'soundbyt')
    op.add_column('downvotes', sa.Column('pitch_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'downvotes', type_='foreignkey')
    op.create_foreign_key('downvotes_pitch_id_fkey', 'downvotes', 'soundbyts', ['pitch_id'], ['id'])
    op.drop_column('downvotes', 'soundbyt_id')
    op.add_column('comments', sa.Column('soundbyts_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'comments', type_='foreignkey')
    op.create_foreign_key('comments_soundbyts_id_fkey', 'comments', 'soundbyts', ['soundbyts_id'], ['id'])
    op.drop_column('comments', 'soundbyt_id')
    # ### end Alembic commands ###
