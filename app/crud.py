from sqlalchemy.orm import Session
from app import models, schemas

def get_all_users(db: Session):
    return db.query(models.Donor).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.Donor).filter(models.Donor.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Donor(name=user.username, password=user.password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_donations(db: Session):
    return db.query(models.Donation).all()

def create_donation(db: Session, donation: schemas.DonationCreate, donor_id: int):
    db_donation = models.Donation(
        amount=donation.amount,
        method=donation.method,
        date=donation.date,
        donor_id=donor_id,
    )
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation
