"""
Lógica de negócio para autenticação e gestão de usuários.
"""
from sqlalchemy.orm import Session
from app.schemas.auth_schema import UserCreate, Login
from app.models.user_model import User
from app.core.security import get_password_hash, verify_password

def create_user(db: Session, user_data: UserCreate) -> User:
    """Cria um novo usuário e faz o hash da senha."""
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username=user_data.username, # Mudança aqui
        # email=user_data.email, # Campo opcional
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str) -> User | None:
    """Busca um usuário pelo username."""
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, login_data: Login) -> User | None:
    """Autentica o usuário pelo username e senha."""
    user = get_user_by_username(db, login_data.username)
    if not user:
        return None
    if not verify_password(login_data.password, user.hashed_password):
        return None
    return user