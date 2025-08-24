from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class PermissionRole(Base):
    __tablename__ = "permission_roles"

    id = Column(Integer, primary_key=True, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    permission = relationship("Permission", backref="permission_roles")
    role = relationship("Role", backref="permission_roles")