from fastapi import APIRouter, status, HTTPException, File, UploadFile, Depends, Header
from backend.schemas import User
from backend.utils import extract_text_from_pdf, extract_text_from_docx
from backend.db import resume_database

router = APIRouter()
allowed_types = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
]


def get_jwt_token(auth: str = Header(None)):
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Error with JWT")
    splits = auth.split()
    token = splits[1]
    return token


@router.post("/api/resume-upload")
async def resume_upload(
    resume_file: UploadFile = File(...), jwt: str = Depends(get_jwt_token)
):
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
    await resume_file.file.seek(0)
    if resume_file.content_type == allowed_types[0]:
        text = extract_text_from_pdf(resume_file.file)
    else:
        text = extract_text_from_docx(resume_file.file)

    resume_database[jwt] = text

    return {"message": "Resume uploaded successfully."}
