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

def create_short_url(db: Session, url_data: URLCreate, user_id: int, max_attempts: int = 5):
    """
    Cria uma URL curta no DB vinculada a um usuário e armazena no cache.
    """
    new_url = None
    for attempt in range(max_attempts):
        code = generate_short_code()
        # Aqui inserimos o owner_id
        new_url = URL(
            original_url=url_data.original_url, 
            short_code=code,
            owner_id=user_id 
        )
        try:
            db.add(new_url)
            db.commit()
            db.refresh(new_url)
            logger.info(f"URL curta criada no DB: {code} para User ID: {user_id}")
            
            # Cache (Read-Through)
            cache_url(new_url.short_code, new_url.original_url)
            
            return new_url
        except IntegrityError:
            db.rollback()
            logger.warning(f"Colisão detectada ({code}), tentando novamente... ({attempt+1}/{max_attempts})")
    
    raise Exception("Falha ao gerar código único")

def get_original_url(db: Session, short_code: str) -> Optional[URL]:
    """
    Retorna a URL original. 
    NOTA: O redirecionamento continua PÚBLICO (não filtra por usuário),
    pois qualquer pessoa com o link deve conseguir acessar.
    """
    # 1. Tenta buscar no cache
    cached_url = get_cached_url(short_code)
    if cached_url:
        logger.debug(f"Cache HIT para short_code: {short_code}")
        # Retorna objeto fake apenas para redirecionamento
        return URL(original_url=cached_url, short_code=short_code, id=0) 

    logger.debug(f"Cache MISS para short_code: {short_code}. Buscando no DB.")
    
    # 2. Se falhar, busca no banco de dados
    url_db = db.query(URL).filter(URL.short_code == short_code).first()
    
    # 3. Se encontrado, atualiza cache
    if url_db:
        cache_url(url_db.short_code, url_db.original_url)
    
    return url_db

def list_urls(db: Session, user_id: int, limit: int = 100):
    """Lista apenas as URLs pertencentes ao usuário logado."""
    return db.query(URL).filter(URL.owner_id == user_id).order_by(URL.created_at.desc()).limit(limit).all()

def delete_url(db: Session, short_code: str, user_id: int) -> bool:
    """
    Deleta uma URL apenas se ela pertencer ao usuário logado.
    """
    # Filtra pelo código E pelo dono
    url = db.query(URL).filter(URL.short_code == short_code, URL.owner_id == user_id).first()
    
    if not url:
        return False
        
    db.delete(url)
    db.commit()
    
    # Invalida cache
    invalidate_url_cache(short_code)
    
    return True