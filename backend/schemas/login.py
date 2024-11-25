from pydantic import BaseModel


# information to log in to an account
class Login(BaseModel):
    email: str
    password: str
