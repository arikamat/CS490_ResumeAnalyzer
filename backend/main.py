from fastapi import FastAPI
from backend.routers import UserRouter  # import the user router
from backend.routers import ResumeUploadRouter

app = FastAPI()

# Include the router with a prefix (optional)
app.include_router(UserRouter)
app.include_router(ResumeUploadRouter)
