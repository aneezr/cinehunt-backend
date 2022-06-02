from fastapi import APIRouter, Body, Depends, Form, status
from fastapi.exceptions import HTTPException
from fastapi.encoders import jsonable_encoder


from models.login import (
    Authdetails,
    Signupdetails
)

from security.security import authenticate_user

from database.login import (
    retrieve_user_data_with_email_id,
    add_user_data_db
)

router = APIRouter()

@router.post('/sign-up/', status_code=status.HTTP_200_OK)
async def create_new_user(userdetails: Signupdetails = Body(...)):
    userdetails = jsonable_encoder(userdetails)
    new_user = await add_user_data_db(data=userdetails)
    if new_user:
        return new_user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User creation failed")

@router.post("/login", status_code=status.HTTP_200_OK)
async def get_access_token(authdetails: Authdetails = Body(...)):
    user_data = await retrieve_user_data_with_email_id(authdetails.username)
    if user_data:
        flag = authenticate_user(authdetails.password, user_data["password"])
        if flag:
            # return user_data
            return {
                "detail": "Login Successfull"
            }
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User data not found")

# @router.post("/reset/password/onetimelinkgen", status_code=status.HTTP_200_OK)
# async def generate_one_time_link(email_id: str = Form(...)):
#     user_data = await retrieve_user_with_email_id(email_id)
#     if user_data:
#         token = createJWT(
#             user_name=None,
#             scope={
#                 "password": ['update']
#             },
#             id = user_data['id'],
#             user_email=email_id,
#             user_type=user_data['user_type']
#         )
#         flag = send_mail(mail_body={
#             'to_addr': email_id,
#             'subject': 'Password Reset Link',
#             'message': 'http://localhost:8000/reset/password/' + token # webhook link of frontent
#         })
#         if flag:
#             return {
#                 'detail': 'Verification link send successfully'
#             }
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email not send")
#     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email Id not found")

# @router.post("/reset/password", status_code=status.HTTP_200_OK)
# async def update_with_new_password(password: str = Form(...), token: str = Depends(JWTBearer(user_type=["password","update"]))):
#     payload = decodeJWT(token)
#     resp = await update_user_password_db(id=payload['id'], user_type=payload['user_type'], data={'password': password})
#     if resp:
#         return {
#             'detail': 'Password reseted successfully'
#         }
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password cannot be updated")