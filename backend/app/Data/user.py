# endpoints/user.py
from fastapi import APIRouter, HTTPException, Depends, status
from models import UserCreate, Token, UserInDB
from database import users_collection
from auth import get_password_hash, create_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/signup", response_model=Token, summary="Register a new user")
async def signup(user: UserCreate):
    # Check if the user already exists.
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password and store the user.
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["hashed_password"] = hashed_password
    user_dict.pop("password", None)  # Remove the plain text password.

    await users_collection.insert_one(user_dict)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token, summary="User login to obtain JWT")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
