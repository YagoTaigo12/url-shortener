import string
import random
import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.url_model import URL
from app.schemas.url_schema import URLCreate
from app.core.redis_client import cache_url, get_cached_url, invalidate_url_cache

logger = logging.getLogger(__name__)
ALPHABET = string.ascii_letters + string.digits

def generate_short_code(length: int = 6) -> str:
    """Gera um código aleatório."""
    return ''.join(random.choices(ALPHABET, k=length))

def create_short_url(db: Session, url_data: URLCreate, max_attempts: int = 5):
    """
    Cria uma URL curta no DB e armazena no cache.
    """
    new_url = None
    for attempt in range(max_attempts):
        code = generate_short_code()
        new_url = URL(original_url=url_data.original_url, short_code=code)
        try:
            db.add(new_url)
            db.commit()
            db.refresh(new_url)
            logger.info(f"URL curta criada no DB: {code}")
            
            # ATUALIZAÇÃO DO CACHE: Armazena a nova URL no Redis (assíncrono/em background se chamado pela rota)
            cache_url(new_url.short_code, new_url.original_url)
            
            return new_url
        except IntegrityError:
            db.rollback()
            logger.warning(f"Colisão detectada ({code}), tentando novamente... ({attempt+1}/{max_attempts})")
    
    raise Exception("Falha ao gerar código único")

def get_original_url(db: Session, short_code: str) -> Optional[URL]:
    """
    Retorna a URL original, priorizando o cache (Read-Through Cache).
    """
    # 1. Tenta buscar no cache
    cached_url = get_cached_url(short_code)
    if cached_url:
        logger.info(f"Cache HIT para short_code: {short_code}")
        # Retorna um objeto URL fake com apenas o campo original_url preenchido
        return URL(original_url=cached_url, short_code=short_code, id=0) 

    logger.info(f"Cache MISS para short_code: {short_code}. Buscando no DB.")
    
    # 2. Se falhar, busca no banco de dados
    url_db = db.query(URL).filter(URL.short_code == short_code).first()
    
    # 3. Se encontrado no DB, armazena no cache para futuras requisições
    if url_db:
        cache_url(url_db.short_code, url_db.original_url)
    
    return url_db

def list_urls(db: Session, limit: int = 100):
    """Lista URLs mais recentes (sem cache para simplificar)."""
    return db.query(URL).order_by(URL.created_at.desc()).limit(limit).all()

def delete_url(db: Session, short_code: str) -> bool:
    """
    Deleta uma URL pelo código curto e invalida o cache.
    """
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if not url:
        return False
        
    db.delete(url)
    db.commit()
    
    # INVALidação DO CACHE: Deleta a chave do Redis (assíncrono/em background se chamado pela rota)
    invalidate_url_cache(short_code)
    
    return True