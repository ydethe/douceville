"""empty message

Revision ID: a65bc325de9e
Revises: 
Create Date: 2020-10-20 19:15:36.620127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a65bc325de9e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "etablissement", "academie", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column("resultat", "admis", existing_type=sa.INTEGER(), nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column("resultat", "admis", existing_type=sa.INTEGER(), nullable=False)
    op.alter_column(
        "etablissement", "academie", existing_type=sa.VARCHAR(), nullable=False
    )
    # ### end Alembic commands ###
