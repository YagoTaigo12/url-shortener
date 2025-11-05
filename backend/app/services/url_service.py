import string
import random
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.url_model import URL
from app.schemas.url_schema import URLCreate

logger = logging.getLogger(__name__)
ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length: int = 6) -> str:
    """Gera um código aleatório."""
    return ''.join(random.choices(ALPHABET, k=length))

def create_short_url(db: Session, url_data: URLCreate, max_attempts: int = 5):
    """Cria uma URL curta evitando colisões."""
    for attempt in range(max_attempts):
        code = generate_short_code()
        new_url = URL(original_url=url_data.original_url, short_code=code)
        try:
            db.add(new_url)
            db.commit()
            db.refresh(new_url)
            logger.info(f"URL curta criada: {code}")
            return new_url
        except IntegrityError:
            db.rollback()
            logger.warning(f"Colisão detectada ({code}), tentando novamente... ({attempt+1}/{max_attempts})")
    raise Exception("Falha ao gerar código único")

def get_original_url(db: Session, short_code: str):
    """Retorna a URL original."""
    return db.query(URL).filter(URL.short_code == short_code).first()

def list_urls(db: Session, limit: int = 100):
    """Lista URLs mais recentes."""
    return db.query(URL).order_by(URL.created_at.desc()).limit(limit).all()

def delete_url(db: Session, short_code: str) -> bool:
    """Deleta uma URL pelo código curto."""
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        return False
    db.delete(url)
    db.commit()
    return True
