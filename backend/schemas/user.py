from pydantic import BaseModel


# User object to save user info
class User(BaseModel):
    email: str
    password: str
    username: str
