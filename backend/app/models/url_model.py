"""
Model SQLAlchemy que representa a tabela 'urls' no banco MySQL.
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base

class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(500), nullable=False)
    short_code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
