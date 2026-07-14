from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# ======================================================
# USER MODEL
# ======================================================

class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    fullname = Column(
        String(100),
        nullable=False
    )


    email = Column(
        String(100),
        unique=True,
        nullable=False
    )


    password = Column(
        String(255),
        nullable=False
    )


    role = Column(
        String(20),
        default="user"
    )


    # Relation avec les documents
    documents = relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete"
    )



# ======================================================
# DOCUMENT MODEL
# ======================================================

class Document(Base):

    __tablename__ = "documents"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    filename = Column(
        String(255),
        nullable=False
    )


    original_filename = Column(
        String(255),
        nullable=False
    )


    file_path = Column(
        String(500),
        nullable=False
    )


    file_type = Column(
        String(50),
        nullable=False
    )


    file_size = Column(
        Integer
    )


    file_hash = Column(
        String(64),
        unique=True,
        nullable=False
    )


    status = Column(
        String(50),
        default="uploaded"
    )


    upload_date = Column(
        DateTime,
        default=datetime.utcnow
    )


    # ============================
    # SECURITY: document owner
    # ============================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    owner = relationship(
        "User",
        back_populates="documents"
    )