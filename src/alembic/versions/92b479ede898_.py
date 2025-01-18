"""empty message

Revision ID: 92b479ede898
Revises: 
Create Date: 2025-01-11 11:43:40.014383

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92b479ede898'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authors',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('biography', sa.String(length=255), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('genres',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('id')
    )
    op.create_table('books',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('publication_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('avaliable_copies', sa.Integer(), nullable=True),
    sa.Column('author', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['authors.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_table('books_genres',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('books', sa.UUID(), nullable=True),
    sa.Column('genres', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['books'], ['books.id'], ),
    sa.ForeignKeyConstraint(['genres'], ['genres.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('books_genres')
    op.drop_table('books')
    op.drop_table('users')
    op.drop_table('genres')
    op.drop_table('authors')
    # ### end Alembic commands ###