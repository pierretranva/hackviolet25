# app/job_postings.py
from fastapi import APIRouter, Header, HTTPException
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models import JobPosting
from app.config import db

router = APIRouter()

# Simple helper to get the current user using a custom header
async def get_current_user(x_username: Optional[str] = Header(None)):
    if not x_username:
        raise HTTPException(status_code=400, detail="x-username header is required")
    user = await db["users"].find_one({"username": x_username})
    if not user:
        raise HTTPException(status_code=400, detail="User not found. Please sign up or login.")
    return user

@router.post("/job-postings", response_model=JobPosting, summary="Create a new job posting")
async def create_job_posting(job: JobPosting, x_username: str = Header(...)):
    current_user = await get_current_user(x_username)
    job.user_id = current_user["_id"]
    # Set the posting date if not provided
    if not job.date:
        job.date = datetime.utcnow()
    job_dict = job.dict(by_alias=True)
    job_dict.pop("_id", None)
    result = await db["job_postings"].insert_one(job_dict)
    job.id = result.inserted_id
    return job

@router.get("/job-postings", response_model=List[JobPosting], summary="Retrieve all job postings for the current user")
async def read_job_postings(x_username: str = Header(...)):
    current_user = await get_current_user(x_username)
    postings = []
    cursor = db["job_postings"].find({"user_id": current_user["_id"]})
    async for document in cursor:
        document["_id"] = str(document["_id"])
        postings.append(JobPosting(**document))
    return postings

@router.get("/job-postings/{job_id}", response_model=JobPosting, summary="Retrieve a specific job posting")
async def read_job_posting(job_id: str, x_username: str = Header(...)):
    current_user = await get_current_user(x_username)
    job = await db["job_postings"].find_one({
        "_id": ObjectId(job_id),
        "user_id": current_user["_id"]
    })
    if not job:
        raise HTTPException(status_code=404, detail="Job posting not found")
    job["_id"] = str(job["_id"])
    return JobPosting(**job)

@router.put("/job-postings/{job_id}", response_model=JobPosting, summary="Update a job posting")
async def update_job_posting(job_id: str, job_update: JobPosting, x_username: str = Header(...)):
    current_user = await get_current_user(x_username)
    update_data = {k: v for k, v in job_update.dict(exclude_unset=True, by_alias=True).items() if k != "_id"}
    result = await db["job_postings"].update_one(
        {"_id": ObjectId(job_id), "user_id": current_user["_id"]},
        {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Job posting not found or no changes made")
    job = await db["job_postings"].find_one({"_id": ObjectId(job_id)})
    job["_id"] = str(job["_id"])
    return JobPosting(**job)

@router.delete("/job-postings/{job_id}", summary="Delete a job posting")
async def delete_job_posting(job_id: str, x_username: str = Header(...)):
    current_user = await get_current_user(x_username)
    result = await db["job_postings"].delete_one({
        "_id": ObjectId(job_id),
        "user_id": current_user["_id"]
    })
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Job posting not found")
    return {"detail": "Job posting deleted"}
