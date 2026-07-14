from pydantic import BaseModel, EmailStr
from datetime import datetime


# ==========================
# USER
# ==========================

class UserRegister(BaseModel):
    fullname: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    fullname: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


# ==========================
# TOKEN
# ==========================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None


# ==========================
# DOCUMENT
# ==========================

class DocumentResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    status: str
    upload_date: datetime

    class Config:
        from_attributes = True