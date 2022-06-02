from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "f669565906612024c22d74227d01f8f41abbb3b351bd20a61977374d92faf555"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def authenticate_user(auth_details_password: str, password : str):
    if not verify_password(auth_details_password, password):
        return False
    return True

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
