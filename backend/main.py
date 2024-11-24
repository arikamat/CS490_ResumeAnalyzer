from fastapi import FastAPI
from backend.routers import UserRouter
from backend.routers import ResumeUploadRouter
from backend.routers import LoginRouter
from backend.routers import JobDescriptionRouter

app = FastAPI()

# Include the router with a prefix (optional)
app.include_router(UserRouter)
app.include_router(ResumeUploadRouter)
app.include_router(LoginRouter)
app.include_router(JobDescriptionRouter)
