from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.core.database import get_db
from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.schemas.auth_schema import UserCreate, UserResponse, Token
from app.services.auth_service import create_user, authenticate_user, get_user_by_username

router = APIRouter(tags=["Auth"], prefix="/auth")

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Rota para registrar um novo usuário."""
    db_user = get_user_by_username(db, user_data.username) # Mudança aqui
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nome de usuário já registrado" # Mudança aqui
        )
    return create_user(db, user_data)

@router.post("/token", response_model=Token)
def login_for_access_token(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Rota para login e geração do token JWT (usa username e password)."""
    # OAuth2PasswordRequestForm usa o campo 'username' que mapeia para o nosso campo 'username'
    login_data = type('LoginData', (object,), {'username': form_data.username, 'password': form_data.password})
    user = authenticate_user(db, login_data)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos", # Mudança aqui
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, # O 'sub' do JWT agora é o username
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}