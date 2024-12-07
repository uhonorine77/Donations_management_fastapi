from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date
from app.database import Base

class Donor(Base):
    __tablename__ = "donors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    password = Column(String)
    is_admin = Column(Integer, default=0)

    donations = relationship("Donation", back_populates="donor")

class Donation(Base):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    method = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    donor_id = Column(Integer, ForeignKey("donors.id"))

    donor = relationship("Donor", back_populates="donations")
