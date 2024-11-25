from fastapi import (
    APIRouter,
    HTTPException,
    File,
    UploadFile,
    Request,
)
from backend.utils import extract_text_from_pdf, extract_text_from_docx
from backend.db import resume_jobdescrip_db
from backend.utils import get_jwt_token

router = APIRouter()
allowed_types = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]


@router.post("/api/resume-upload")
async def resume_upload(request: Request, resume_file: UploadFile = File(...)):
    """
    REST endpoint to upload resume file, extract its text, and store in in-memory db

    Args:
        request (Request): Request object
        resume_file (UploadFile): Uploaded Resume file - must be pdf or docx
    """

    jwt = get_jwt_token(request)
    if resume_file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Only PDF or DOCX files are allowed.",
        )
    fileContents = await resume_file.read()
    size = len(fileContents)
    if size > 2000000:
        raise HTTPException(status_code=400, detail="File size is over 2MB.")

    text = ""
    resume_file.file.seek(0)
    if resume_file.content_type == allowed_types[0]:
        text = extract_text_from_pdf(resume_file.file)
    else:
        text = extract_text_from_docx(resume_file.file)

    if jwt not in resume_jobdescrip_db:
        resume_jobdescrip_db[jwt] = {}
    resume_jobdescrip_db[jwt]["resume_text"] = text

    return {"message": "Resume uploaded successfully."}
