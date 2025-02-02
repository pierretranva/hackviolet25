# app/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.auth import router as auth_router
from app.job_postings import router as job_postings_router

app = FastAPI(title="Job Application API")

# Configure CORS (adjust allowed origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for signup/login and job postings
app.include_router(auth_router, tags=["Authentication"])
app.include_router(job_postings_router, tags=["Job Postings"])

# Global error handler (optional)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred."}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
