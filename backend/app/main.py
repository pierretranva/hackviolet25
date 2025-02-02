from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
from typing import List

from fastapi.middleware.cors import CORSMiddleware

from ollama.llm_integration import LLMIntegration
from webscrape import WebScrape


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

class UploadDescriptionPayload(BaseModel):
    description: str


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
    penguAI = LLMIntegration(model="deepseek-r1:1.5b")
    job_url = "https://www.linkedin.com/jobs/view/4139906168/?alternateChannel=search&refId=Gmoziy9CPHHdQ%2B3XSqLrnQ%3D%3D&trackingId=pJrlfbjMos6lPPfEWPj0cQ%3D%3D" #mongodb grab
    resume_pdf = "" ##mongodb grab

    sample_resume_pdf = "Resume2.pdf"
    # Specify the output markdown file path
    output_markdown_file = "UpdatedResume2.md"

    corvScraper = WebScrape(job_url)
    job_description = corvScraper.scrape()
    print(job_description)

    try:
         modified_resume = penguAI.transform_resume(job_description, sample_resume_pdf)
         md_resume_new = modified_resume
        
         markdown_resume = penguAI.string_to_markdown(modified_resume, output_markdown_file) ##ask sam how this output markdown file thing works im too tired to figure it out
         ##chuck the markdown_resume into mongodb
    except:
        print("what")

    mongo_id = "whatever mongo is for the new resume"
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
    
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        # print(file_data)
        file_id = "temp12345"
        # file_id = fs.put(file_data, filename=file.filename, content_type=file.content_type)
        return {"message": "File uploaded successfully!", "file_id": str(file_id)}
    except Exception as e:
        return {"error": str(e)}

@app.post("/upload-description")
async def upload_description(description: UploadDescriptionPayload ):
    try:
        print(description.description)
        return {"message": "Description uploaded successfully!"}
    except Exception as e:
        return {"error": str(e)}
    
@app.get("/get-description")
def get_description():
    try:
        # get from db
        return {"description": "This is a job description"}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/edit-resume")
def edit_resume(request: EditResumePayload):
    try:
        mongo_id, md_resume_new = edit_resume_request(request.job_mongo_id, request.personal_info_mongo_id)
        return {"new_resume_mongo_id": mongo_id, "new_resume": md_resume_new}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=False)
