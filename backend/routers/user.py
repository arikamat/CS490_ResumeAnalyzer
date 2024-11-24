from fastapi import APIRouter, status, HTTPException
from backend.schemas import User
import bcrypt

router = APIRouter()

# initialize set to save emails and database to store info
email_set = set()
database = {}


@router.post("/api/register", status_code=status.HTTP_201_CREATED)
async def create_user_profile(user: User):
    '''
        Creates a user profile

        Args: 
            User object: Holds information inputted by the user

        Returns: 
            Dict: message detailing the status of the user creation

    '''
    # if duplicate email then throw error
    if user.email in email_set:
        raise HTTPException(status_code=400, detail="Email is not unique")
    email_set.add(user.email)

    # encrypt password and save to database
    encrypted_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    database[user.email] = {
        "email": user.email,
        "password": encrypted_password,
        "username": user.username,
    }
    return {"message": "User registered"}
