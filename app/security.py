from pwdlib import PasswordHash
import jwt
from dotenv import load_dotenv
import os
import uuid
import datetime



load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")

password_hasher = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hasher.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hasher.verify(password, hashed_password)

def create_access_token(user_id: uuid.UUID):
    return jwt.encode(
        {"sub": str(user_id),
         "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=600)}, 
        JWT_SECRET, 
        algorithm="HS256",
    )

def decode_access_token(token: str):
    return jwt.decode(
        token, 
        JWT_SECRET,
        algorithms=["HS256"]
    )

    