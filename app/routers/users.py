import uuid

from fastapi import HTTPException, APIRouter, Depends
from app.database import get_session
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserResponse, UserLogin
from app.models import UserDB
from app.security import hash_password, verify_password, create_access_token
from app.dependencies import get_current_user

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


@router.post("/login")
def user_login(user: UserLogin, session: Session = Depends(get_session)):

    found_user = session.scalar(
        select(UserDB).where(
            UserDB.email == user.email
        )
    )

    if found_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    is_correct = verify_password(user.password, found_user.password_hash)

    if not is_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(found_user.id)

    return {
        "access_token" : token,
        "token_type" : "bearer"
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: UserDB = Depends(get_current_user)):

    return current_user






