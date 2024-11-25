from pydantic import BaseModel
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    is_admin: Optional[int] = 0

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class DonationBase(BaseModel):
    amount: float
    method: str
    date: str

class DonationCreate(DonationBase):
    donor_id: int

class Donation(DonationBase):
    id: int

    class Config:
        orm_mode = True
