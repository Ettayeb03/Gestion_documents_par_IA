from dotenv import load_dotenv
import os

load_dotenv()

# ==========================
# PostgreSQL Configuration
# ==========================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================
# JWT Configuration
# ==========================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "pfa_bcs_document_intelligence_2026_secret_key"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60