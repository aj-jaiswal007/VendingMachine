from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, relationship

from vendingmachine.common.database import AuditMixin, Base


class Product(AuditMixin, Base):
    __tablename__ = "vm_product"
    created_by = mapped_column(Integer, ForeignKey("vm_users.id", ondelete="CASCADE"))
    name = Column(String)
    description = Column(String)
    price = Column(Integer)


class Inventory(AuditMixin, Base):
    __tablename__ = "vm_inventory"
    product_id = mapped_column(Integer, ForeignKey("vm_product.id", ondelete="CASCADE"), unique=True)
    quantity = Column(Integer)
    product = relationship("Product", backref="inventory")
