"""empty message

Revision ID: 54e1a8340d29
Revises: 
Create Date: 2020-10-22 08:37:37.991482

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54e1a8340d29'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('resultat',
    sa.Column('idx', sa.Integer(), nullable=False),
    sa.Column('diplome', sa.String(length=191), nullable=False),
    sa.Column('annee', sa.Integer(), nullable=False),
    sa.Column('presents', sa.Integer(), nullable=False),
    sa.Column('admis', sa.Integer(), nullable=True),
    sa.Column('mentions', sa.Integer(), nullable=True),
    sa.Column('etablissement_id', sa.String(length=10), nullable=False),
    sa.ForeignKeyConstraint(['etablissement_id'], ['etablissement.UAI'], ),
    sa.PrimaryKeyConstraint('idx'),
    sa.UniqueConstraint('diplome', 'annee', 'etablissement_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('resultat')
    # ### end Alembic commands ###
