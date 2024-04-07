from vendingmachine.common.database import AuditMixin, Base
from sqlalchemy import Column, String, Boolean, Enum
from vendingmachine.user.enums import RoleName


class User(AuditMixin, Base):
    __tablename__ = "vm_users"

    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(RoleName), default=RoleName.BUYER)
