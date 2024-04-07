from sqlalchemy import Column, Float, ForeignKey, Integer, String

from vendingmachine.common.database import AuditMixin, Base


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
