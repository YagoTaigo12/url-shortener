"""
Contém a lógica principal de encurtamento e recuperação de URLs.
"""
from sqlalchemy.orm import Session
from app.models.url_model import URL
from app.schemas.url_schema import URLCreate
import string, random

def generate_short_code(length: int = 6) -> str:
    """Gera um código aleatório de 6 caracteres."""
    # Garante que o código seja único (em produção, um loop de retry seria necessário)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_short_url(db: Session, url_data: URLCreate):
    """Cria e salva uma nova URL encurtada no banco."""
    # A URL curta deve ser o nome do host + short_code. Aqui salvamos apenas o código.
    short_code = generate_short_code()
    new_url = URL(original_url=url_data.original_url, short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def get_original_url(db: Session, short_code: str):
    """Busca a URL original pelo código curto."""
    return db.query(URL).filter(URL.short_code == short_code).first()
