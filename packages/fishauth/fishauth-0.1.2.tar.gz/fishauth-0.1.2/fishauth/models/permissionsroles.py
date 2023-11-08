from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Table
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func
from fishauth.models.base import Base


permissionsroles = Table(
    "permissionsroles",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("role_id", Integer, ForeignKey("role.id", ondelete="CASCADE")),
    Column("permissions_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE")),
    Column("time_created", DateTime(timezone=True), server_default=func.now()),
    Column("time_updated", DateTime(timezone=True), onupdate=func.now()),
    UniqueConstraint("role_id", "permissions_id"),
)
