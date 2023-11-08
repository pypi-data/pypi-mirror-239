from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from fishauth.models.base import Base
from fishauth.models.organization import Organization


class User(Base):
    # __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(
        Integer,
        ForeignKey("organization.id", deferrable=True, initially="DEFERRED"),
        nullable=True,
        index=True,
    )
    title = Column(String, index=True)
    names = Column(String, index=True, nullable=False)
    last_name = Column(String, index=True, nullable=False)
    mother_last_name = Column(String)
    genero_id = Column(
        Integer,
        ForeignKey("genero.id", deferrable=True, initially="DEFERRED"),
        nullable=True,
    )

    sexo_id = Column(
        Integer,
        ForeignKey("sexo.id", deferrable=True, initially="DEFERRED"),
        nullable=True,
    )
    email = Column(String, index=True, nullable=False)
    password = Column(String, nullable=True)
    is_active = Column(Boolean(), default=True)
    birth_date = Column(Date, nullable=True)
    phone_mobile = Column(String(20), nullable=True)
    avatar = Column(String, nullable=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    organization = relationship("Organization", back_populates="members")

    def __str__(self):
        return f"{self.names} {self.last_name} {self.mother_last_name}"
