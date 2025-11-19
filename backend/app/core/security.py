"""
Funções utilitárias de segurança: Hashing de senha e JWT.
"""
from datetime import datetime, timedelta, timezone
from typing import Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Esquemas de Autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# Configuração de Hashing de Senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
BCRYPT_MAX_BYTES = 72 # Limite de 72 bytes do bcrypt

# Configurações de JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- Funções de Senha ---

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    # Trunca a senha se necessário antes de verificar
    secret = plain_password[:BCRYPT_MAX_BYTES]
    return pwd_context.verify(secret, hashed_password)

def get_password_hash(password: str) -> str:
    """Retorna o hash de uma senha em texto plano."""
    # Trunca a senha se for maior que 72 bytes antes de hashear
    secret = password[:BCRYPT_MAX_BYTES]
    return pwd_context.hash(secret)

# --- Funções de JWT ---

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
# ... (restante da função inalterada)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict[str, Any]:
# ... (restante da função inalterada)
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas ou token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Dependência de Autenticação ---

def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
# ... (restante da função inalterada)
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username