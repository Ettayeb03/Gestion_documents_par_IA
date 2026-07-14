from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import UserRegister, UserResponse, Token
from security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# ======================================================
# REGISTER
# ======================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserRegister,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists."
        )

    new_user = User(
        fullname=user.fullname,
        email=user.email,
        password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



# ======================================================
# LOGIN
# ======================================================

@router.post(
    "/login",
    response_model=Token
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()


    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )


    if not verify_password(
        form_data.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )


    access_token = create_access_token(
        data={
            "sub": db_user.email,
            "user_id": db_user.id,
            "role": db_user.role
        }
    )


    return {
        "access_token": access_token,
        "token_type": "bearer"
    }



# ======================================================
# CURRENT USER
# ======================================================

@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user



# ======================================================
# LOGOUT
# ======================================================

@router.post("/logout")
def logout():

    return {
        "message": "Logout successful. Remove the JWT token from client storage."
    }