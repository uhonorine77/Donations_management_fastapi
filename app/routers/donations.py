from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
async def get_donations(db: Session = Depends(get_db)):
    donations = crud.get_donations(db)
    return donations

@router.post("/")
async def create_donation(donation: schemas.DonationCreate, db: Session = Depends(get_db)):
    donor = crud.get_user_by_id(db, donation.donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found")
    created_donation = crud.create_donation(db, donation, donation.donor_id)
    return created_donation
