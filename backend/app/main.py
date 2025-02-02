from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI(title="PenguAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobAddPayload(BaseModel):
    company_name: str
    date: str  # Enforce a stricter date format later if needed
    url: str
    chips: List[str]

class AddResumeAndOtherInfoPayload(BaseModel):
    resume_add: str
    additional_info: str

class EditResumePayload(BaseModel):
    job_mongo_id: str
    personal_info_mongo_id: str


def process_job_request(company_name: str, date: str, url: str, chips: List[str]):
    ##write the code to process the job request
    mongo_id = "temp12345"
    job_description = f"Job at {company_name} on {date}. More info: {url}"
    return mongo_id, job_description

def add_personal_info_request (resume_add: str, additional_info: str):
    ##write the code to add the personal info requests into the mongo db
    mongo_id = resume_add + additional_info
    return mongo_id

def edit_resume_request(job_mongo_id: str, personal_info_mongo_id: str):
    mongo_id = personal_info_mongo_id
    md_resume_new = f"{job_mongo_id} - Woah, nice resume!"
    return mongo_id, md_resume_new


@app.get("/")
def read_root():
    return {"message": "Welcome to PenguAPI. Im gonna touch Sam"}

@app.post("/add-job")
def process_job(request: JobAddPayload):
    try:
        mongo_id, job_description = process_job_request(
            request.company_name, request.date, request.url, request.chips
        )
        return {"new_job_mongo_id": mongo_id, "job_description": job_description}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-personal-info")
def add_personal_info(request: AddResumeAndOtherInfoPayload):
    try:
        mongo_id = add_personal_info_request(request.resume_add, request.additional_info)
        return {"personal_info_mongo_id": mongo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/edit-resume")
def edit_resume(request: EditResumePayload):
    try:
        mongo_id, md_resume_new = edit_resume_request(request.job_mongo_id, request.personal_info_mongo_id)
        return {"new_resume_mongo_id": mongo_id, "new_resume": md_resume_new}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
