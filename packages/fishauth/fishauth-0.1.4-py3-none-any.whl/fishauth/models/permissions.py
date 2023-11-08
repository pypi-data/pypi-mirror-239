from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from fishauth.models.base import Base


class Permissions(Base):
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    name = Column(String, unique=True, index=True, nullable=False)
    is_system = Column(Boolean(), default=False, nullable=True)
    aplication_id = Column(Integer, ForeignKey("application.id"), nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    app = relationship("Application", back_populates="permissions_app")

    def __str__(self):
        return f"{self.label} ({self.name})"
