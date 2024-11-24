from fastapi import FastAPI
from backend.routers import UserRouter  # import the user router
from backend.routers import ResumeUploadRouter
from backend.routers import LoginRouter  # import the user router

app = FastAPI()

# Include the router with a prefix (optional)
app.include_router(UserRouter)
app.include_router(ResumeUploadRouter)
app.include_router(LoginRouter)
