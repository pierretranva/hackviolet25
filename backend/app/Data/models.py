# app/models.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

# Helper class for MongoDB ObjectId conversion
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# User models
class UserIn(BaseModel):
    username: str
    password: str  # (In this simplified version, passwords are stored in plain text.)

class UserOut(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# Chip model for job posting chips
class Chip(BaseModel):
    text: str
    color: str  # e.g., "bg-blue-500" (a Tailwind CSS class)

# Job Posting model
class JobPosting(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    name: str
    date: datetime = Field(default_factory=datetime.utcnow)
    link_url: str
    markdown_resume: Optional[str] = None
    chips: Optional[List[Chip]] = []
    ai_reasoning: Optional[str] = None
    user_id: Optional[PyObjectId] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}