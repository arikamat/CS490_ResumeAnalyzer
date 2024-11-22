from fastapi import APIRouter, File, UploadFile, HTTPException

router = APIRouter(
    prefix="/api"
)

@router.post("/resume-upload")
async def resume_upload(resume_file: UploadFile = File(...)):
    if resume_file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Only pdf, doc, and docx files are allowed")
    fileContents = await resume_file.read()
    size = len(fileContents)
    allowed_types = ["application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    
    if size>2000000:
        raise HTTPException(status_code=400, detail="File Size must be less than 2MB")