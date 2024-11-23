from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import bcrypt

#User object to save user info
class User(BaseModel):
    email: str
    password: str
    username: str

#initialize set to save emails and database to store info
email_set = set()
database = {}

app = FastAPI()

@app.post("/api/register",status_code=status.HTTP_201_CREATED)
async def create_user_profile(user: User):
    #if duplicate email then throw error
    if user.email in email_set:
        raise HTTPException(status_code=400, detail="Email is not unique")
    email_set.add(user.email)

    #encrypt password and save to database
    encrypted_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    database[user.email] = {
        "email":user.email,
        "password":encrypted_password,
        "username":user.username
    }
    return { "message": "User registered" }

