"""
Schemas Pydantic usados para validação de entrada e saída de dados de Autenticação.
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime

# --- Usuário ---

class UserBase(BaseModel):
    username: str
    # email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Autenticação JWT ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    # Subject do JWT
    # email: str | None = None
    username: str | None = None

class Login(UserBase):
    password: str