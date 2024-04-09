"""one-one relationship b/w invectory and product

Revision ID: 5eade0279df7
Revises: 3a989a654ec1
Create Date: 2024-04-09 23:23:26.715966

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5eade0279df7"
down_revision: Union[str, None] = "3a989a654ec1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "vm_inventory", ["product_id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "vm_inventory", type_="unique")
    # ### end Alembic commands ###
