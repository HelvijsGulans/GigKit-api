from app.security import decode_access_token
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_session
from app.models import UserDB
import uuid
from jwt import InvalidTokenError


bearer = HTTPBearer()

def get_token_from_request(credentials: HTTPAuthorizationCredentials = Depends(bearer)):

    return credentials.credentials

def get_user_id_from_token(token = Depends(get_token_from_request)):

    try:
        payload = decode_access_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    user_id = uuid.UUID(payload["sub"])

    return user_id

def get_current_user(user_id = Depends(get_user_id_from_token), session: Session = Depends(get_session)):

    user = session.get(UserDB, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user