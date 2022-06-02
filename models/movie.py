from typing import List
from fastapi.param_functions import Form
from pydantic import BaseModel, EmailStr, Field

# class AddMovieDetail(BaseModel):
#     name: str = Form(...)
#     designation: str = Form(...)
#     email_id: EmailStr = Form(...)
#     phone_no: str = Form(...)
#     address: str = Form(...)
#     country: str = Form(...)
#     department: str = Form(...)
#     emp_id: str = Form(...)
#     password: str = Form(...)
class movie_ids(BaseModel):
    movie_names: List[str] = Form(...)

class Moviegeneration(BaseModel):
    title: str = Form(...)
    count: int = Form(...)

class CF(BaseModel):
    usermovieids: List[int] = Form(...)
    usermovierates: List[int] = Form(...)
    num: int = Form(...)

def movie_helper(data) -> dict:
    return {
        "id": str(data["_id"]),
        # "movieId": data["movieId"],
        "title": data["title"],
        "genres": data['genres']
    }