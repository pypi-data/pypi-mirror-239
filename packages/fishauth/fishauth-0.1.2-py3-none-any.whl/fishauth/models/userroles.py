from sqlalchemy import Column, Integer, DateTime, Table, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.sql import func
from fishauth.models.base import Base


usersroles = Table(
    "usersroles",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("role_id", Integer, ForeignKey("role.id", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey("user.id", ondelete="CASCADE")),
    Column("time_created", DateTime(timezone=True), server_default=func.now()),
    Column("time_updated", DateTime(timezone=True), onupdate=func.now()),
    UniqueConstraint("role_id", "user_id"),
)
