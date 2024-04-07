from vendingmachine.common.database import AuditMixin, Base
from sqlalchemy import Column, Integer, ForeignKey, String, Float


class Product(AuditMixin, Base):
    __tablename__ = "vm_product"
    created_by = Column(Integer, ForeignKey("vm_users.id"))
    name = Column(String)
    description = Column(String)
    price = Column(Float)


class Inventory(AuditMixin, Base):
    __tablename__ = "vm_inventory"
    product_id = Column(Integer, ForeignKey("vm_product.id"))
    quantity = Column(Integer)
