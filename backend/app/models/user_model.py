"""
Model SQLAlchemy que representa a tabela 'users' no banco MySQL.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True, nullable=False) # Mudança aqui
    # email = Column(String(255), index=True, nullable=True) # Mantido, mas não único
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relação opcional: Se quiser ligar URLs a um usuário (Futuro)
    urls = relationship("URL", back_populates="owner")