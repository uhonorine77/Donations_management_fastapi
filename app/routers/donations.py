from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/donations/list/")
async def get_donations(db: Session = Depends(get_db)):
    donations = crud.get_donations(db)
    return donations

@router.get("/donations/{donation_id}/", response_model=schemas.Donation)
async def get_donation_by_id(donation_id: int, db: Session = Depends(get_db)):
    donation = crud.get_donation_by_id(db, donation_id)
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found!")
    return donation

@router.post("/donations/")
async def create_donation(donation: schemas.DonationCreate, db: Session = Depends(get_db)):
    donor = crud.get_user_by_id(db, donation.donor_id)
    if not donor:
        raise HTTPException(status_code=404, detail="Donor not found!")
    created_donation = crud.create_donation(db, donation, donation.donor_id)
    return created_donation
