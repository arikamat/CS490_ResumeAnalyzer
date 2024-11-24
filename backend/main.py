from fastapi import FastAPI
from backend.routers import UserRouter  # import the user router

app = FastAPI()

# Include the router with a prefix (optional)
app.include_router(UserRouter)
