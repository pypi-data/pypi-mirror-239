from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from fishauth.models.base import Base


class Role(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    aplication_id = Column(
        Integer,
        ForeignKey(
            "application.id", ondelete="CASCADE", deferrable=True, initially="DEFERRED"
        ),
        nullable=False,
    )
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __str__(self):
        return "%s" % (self.name)
