from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from fishauth.models.base import Base


class Application(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False, unique=True)
    url = Column(String(256), nullable=True)
    is_active = Column(Boolean(), default=True)
    type_entity = Column(Integer, index=True, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    permissions_app = relationship("Permissions", back_populates="app")

    def __str__(self):
        return "%s" % (self.name)
