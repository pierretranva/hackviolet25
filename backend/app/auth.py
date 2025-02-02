# app/auth.py
from fastapi import APIRouter, HTTPException
from backend.app.API.models import UserIn
from app.config import db

router = APIRouter()

@router.post("/signup", summary="Register a new user")
async def signup(user: UserIn):
    # Check if the username already exists
    existing_user = await db["users"].find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    # Store the user (plain text password for simplicity)
    user_doc = {"username": user.username, "password": user.password}
    await db["users"].insert_one(user_doc)
    
    return {"message": "User created successfully", "username": user.username}

@router.post("/login", summary="User login")
async def login(user: UserIn):
    db_user = await db["users"].find_one({"username": user.username})
    if not db_user or db_user["password"] != user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"message": "Login successful", "username": user.username}