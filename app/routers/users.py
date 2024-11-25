from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return schemas.User(id=db_user.id, username=db_user.name, is_admin=db_user.is_admin)


@router.get("/users/list", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db)
    return [schemas.User(id=user.id, username=user.name, is_admin=user.is_admin) for user in users]


@router.get("/users/list/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return schemas.User(id=user.id, username=user.name, is_admin=user.is_admin)

