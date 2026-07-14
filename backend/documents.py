from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from database import get_db
from models import Document, User
from security import get_current_user

import os
import uuid
import shutil
import hashlib
import mimetypes


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_FOLDER = "../uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)



def calculate_file_hash(file_path):

    hash_md5 = hashlib.md5()

    with open(file_path, "rb") as f:

        for chunk in iter(lambda: f.read(8192), b""):

            hash_md5.update(chunk)

    return hash_md5.hexdigest()



# ======================================================
# UPLOAD
# ======================================================

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    extension = os.path.splitext(file.filename)[1].lower()

    unique_filename = f"{uuid.uuid4()}{extension}"


    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )


    try:

        with open(file_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )


        file_hash = calculate_file_hash(file_path)


        existing = db.query(Document).filter(
            Document.file_hash == file_hash
        ).first()


        if existing:

            os.remove(file_path)

            raise HTTPException(
                status_code=409,
                detail="Document already exists"
            )



        mime_type = mimetypes.guess_type(
            file.filename
        )[0] or "application/octet-stream"



        document = Document(

            filename=unique_filename,

            original_filename=file.filename,

            file_path=file_path,

            file_type=mime_type,

            file_size=os.path.getsize(file_path),

            file_hash=file_hash,

            status="uploaded",

            user_id=current_user.id
        )


        db.add(document)

        db.commit()

        db.refresh(document)


        return {

            "message": "Document uploaded successfully",

            "document_id": document.id,

            "filename": document.original_filename

        }


    except Exception as e:

        if os.path.exists(file_path):

            os.remove(file_path)

        raise e




# ======================================================
# GET USER DOCUMENTS
# ======================================================

@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()



# ======================================================
# GET ONE
# ======================================================

@router.get("/{document_id}")
def get_document(
    document_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()


    if not document:

        raise HTTPException(
            404,
            "Document not found"
        )


    return document




# ======================================================
# VIEW
# ======================================================

@router.get("/{document_id}/view")
def view_document(
    document_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()


    if not document:

        raise HTTPException(
            404,
            "Document not found"
        )


    allowed = [
        "application/pdf",
        "image/png",
        "image/jpeg"
    ]


    if document.file_type not in allowed:

        raise HTTPException(
            400,
            "Preview not supported"
        )


    return FileResponse(
        document.file_path,
        media_type=document.file_type
    )




# ======================================================
# DOWNLOAD
# ======================================================

@router.get("/{document_id}/download")
def download_document(
    document_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()


    if not document:

        raise HTTPException(
            404,
            "Document not found"
        )


    return FileResponse(
        document.file_path,
        filename=document.original_filename,
        media_type="application/octet-stream"
    )




# ======================================================
# DELETE
# ======================================================

@router.delete("/{document_id}")
def delete_document(
    document_id:int,
    db:Session = Depends(get_db),
    current_user:User = Depends(get_current_user)
):

    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()


    if not document:

        raise HTTPException(
            404,
            "Document not found"
        )


    if os.path.exists(document.file_path):

        os.remove(document.file_path)


    db.delete(document)

    db.commit()


    return {
        "message":"Document deleted successfully"
    }