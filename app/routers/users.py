import uuid

from fastapi import FastAPI, HTTPException, APIRouter, Depends
from app.database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse
from app.models import UserDB
from app.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("", status_code=201, response_model=UserResponse)
def register_user(user: UserCreate, session: Session = Depends(get_session)):

    existing_user = session.scalar(
        select(UserDB).where(
            UserDB.email == user.email
        )
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = UserDB(
        email = user.email,
        password_hash = hashed_password
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user