from fastapi import (
    APIRouter,
    HTTPException,
    Request,
)
from backend.db import resume_jobdescrip_db
from backend.utils import get_jwt_token
from backend.schemas import JobDescription

router = APIRouter()

@router.post("/api/job-description")
async def resume_upload(description: JobDescription, request: Request):
    """
    REST endpoint to upload job description, ensure it is less than 5000 characters, and store in in-memory db

    Args:
        description (JobDescription): Description sent in request
        request (Request): Request Object
    """
    jwt = get_jwt_token(request)
    text = description.job_description.strip()
    if len(text)>5000:
        raise HTTPException(
            status_code=400,
            detail="Job description exceeds character limit.",
        )

    if jwt not in resume_jobdescrip_db:
        resume_jobdescrip_db[jwt] = {}
    resume_jobdescrip_db[jwt]["job_description"] = text

    return {"message": "Job description submitted successfully."}
