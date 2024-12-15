from fastapi import FastAPI
from backend.routers import UserRouter
from backend.routers import ResumeUploadRouter
from backend.routers import LoginRouter
from backend.routers import JobDescriptionRouter
from backend.routers import UserInputRouter
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",  # React frontend
   " http://127.0.0.1:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # Allows cookies and authentication headers
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all HTTP headers
)

# Include the router with a prefix (optional)
app.include_router(UserRouter)
app.include_router(ResumeUploadRouter)
app.include_router(LoginRouter)
app.include_router(JobDescriptionRouter)
app.include_router(UserInputRouter)
