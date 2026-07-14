from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from schemas import UserResponse, UserRegister
from security import (
    get_current_user,
    hash_password
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# ======================================================
# GET ALL USERS (ADMIN)
# ======================================================

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )

    db: Session = SessionLocal()

    try:
        return db.query(User).all()

    finally:
        db.close()


# ======================================================
# GET USER BY ID
# ======================================================

@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if current_user.role != "admin" and current_user.id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        return user

    finally:
        db.close()


# ======================================================
# UPDATE USER
# ======================================================

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserRegister,
    current_user: User = Depends(get_current_user)
):

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        if current_user.role != "admin" and current_user.id != user.id:
            raise HTTPException(
                status_code=403,
                detail="Access denied"
            )

        existing_email = db.query(User).filter(
            User.email == user_data.email,
            User.id != user_id
        ).first()

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        user.fullname = user_data.fullname
        user.email = user_data.email

        if user_data.password:
            user.password = hash_password(user_data.password)

        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


# ======================================================
# CHANGE ROLE (ADMIN)
# ======================================================

@router.put("/{user_id}/role")
def change_role(
    user_id: int,
    role: str,
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Only admin can change roles"
        )

    if role not in ["admin", "user"]:
        raise HTTPException(
            status_code=400,
            detail="Role must be 'admin' or 'user'"
        )

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        user.role = role

        db.commit()
        db.refresh(user)

        return {
            "message": "Role updated successfully",
            "user": {
                "id": user.id,
                "fullname": user.fullname,
                "email": user.email,
                "role": user.role
            }
        }

    finally:
        db.close()


# ======================================================
# DELETE USER (ADMIN)
# ======================================================

@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user)
):

    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    db: Session = SessionLocal()

    try:

        user = db.query(User).filter(
            User.id == user_id
        ).first()

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        db.delete(user)
        db.commit()

        return {
            "message": "User deleted successfully"
        }

    finally:
        db.close()