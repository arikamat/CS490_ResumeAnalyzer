from fastapi import APIRouter, status, HTTPException
from backend.schemas import Login
import bcrypt
from .user import database
from .user import router
from datetime import datetime, timedelta
import jwt

router = APIRouter()


@router.post("/api/login")
async def check_login(login: Login):
    '''
        Implements login and makes a JWT token

        Args: 
            Login object: Contains email and password inputted by the user

        Returns: 
            Dict: A JWT token
    '''
    
    #if no account with the given email
    if login.email not in database:
        raise HTTPException(status_code=400, detail="No account associated with this email")

    #if the password given is not the correct password
    if not bcrypt.checkpw(login.password.encode("utf-8"), database[login.email]["password"] ):
        raise HTTPException(status_code=400, detail="Incorrect password")

    #create payload for jwt token that will expire in 15 minutes
    payload = {
        "email": login.email,
        "exp": datetime.utcnow() + timedelta(hours=.25)
    }

    #generate the token with the payload and secret key "spongebob"
    token = jwt.encode(payload, "spongebob", algorithm="HS256")
      
    return { "token": token }
