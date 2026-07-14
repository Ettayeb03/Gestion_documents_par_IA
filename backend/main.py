from fastapi import FastAPI

from database import engine
from models import Base

from auth import router as auth_router
from users import router as users_router
from documents import router as documents_router


# Création des tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Document Intelligence API",
    version="1.0.0"
)



# ==============================
# ROUTERS
# ==============================

app.include_router(auth_router)

app.include_router(users_router)

app.include_router(documents_router)



# ==============================
# ROOT
# ==============================

@app.get("/")
def root():

    return {
        "message": "Document Intelligence API is running 🚀"
    }