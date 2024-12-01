from pydantic import BaseModel


# Object to save the resume text and job description
class UserInput(BaseModel):
    resume_text: str
    job_description: str
