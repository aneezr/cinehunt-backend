from pydantic import BaseModel, EmailStr
from typing import Optional, List

class Signupdetails(BaseModel):
    first_name : str
    last_name : str
    email_id : EmailStr
    password: str

class Authdetails(BaseModel):
    username : str
    password: str

def user_login_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        "first_name": data["first_name"],
        "last_name": data['last_name'],
        "email_id": data['email_id'],
        "password": data['password'],
    }