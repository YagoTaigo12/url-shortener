"""
Gerencia a conexão com o banco de dados MySQL via SQLAlchemy.
Cria o engine e a SessionLocal para operações de CRUD.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Gera uma sessão de banco para uso em endpoints."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
