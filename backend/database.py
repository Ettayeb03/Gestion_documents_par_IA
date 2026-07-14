from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_URL


# Connexion PostgreSQL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,     # Vérifie que la connexion est encore active
    pool_size=10,           # Nombre de connexions gardées ouvertes
    max_overflow=20         # Connexions supplémentaires autorisées
)


# Gestion des sessions SQLAlchemy
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Classe de base pour les modèles
Base = declarative_base()


# Dépendance FastAPI
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()