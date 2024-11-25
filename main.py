from fastapi import FastAPI

from app.routers import donations, users


app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(donations.router, prefix="/donations", tags=["donations"])

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Donation Management System!"}

@app.get("/favicon.ico")
async def favicon():
    return {"message": "No favicon set yet."}
