from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from fishauth.models.base import Base
from sqlalchemy.orm import relationship


class Organization(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), unique=True, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    members = relationship("User", back_populates="organization")

    def __str__(self):
        return "%s" % (self.name)
