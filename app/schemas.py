from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserBase(BaseModel):
    username: str
    is_admin: Optional[int] = 0

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    username: str
    is_admin: Optional[int] = 0
    class Config:
        from_attributes = True

class DonationBase(BaseModel):
    amount: float
    method: str
    date: date

class DonationCreate(DonationBase):
    donor_id: int

class Donation(DonationBase):
    id: int
    donor_id: int
    class Config:
        from_attributes = True
