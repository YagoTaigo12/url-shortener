import redis
import logging
from app.core.config import settings
from typing import Optional

logger = logging.getLogger(__name__)

# Configurações do Redis lidas do .env via config.py
REDIS_HOST: str = settings.REDIS_HOST
REDIS_PORT: int = settings.REDIS_PORT
# Tempo de vida do cache para uma URL (24 horas)
CACHE_TTL_SECONDS: int = 3600 * 24

redis_client: Optional[redis.Redis] = None

def get_redis_client() -> Optional[redis.Redis]:
    """
    Retorna a instância do cliente Redis.
    Se a conexão falhar, retorna None para permitir que o serviço continue
    operando sem cache (falha suave).
    """
    global redis_client
    
    # Se o cliente já foi inicializado (mesmo que seja None após uma falha)
    if redis_client is not None:
        return redis_client
    
    # Se ainda não tentamos conectar
    try:
        # Tenta conectar
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=0, # Usando o banco de dados 0
            decode_responses=True, # Decodifica automaticamente para string (valor da URL)
            socket_connect_timeout=3, # Tempo limite de conexão
            socket_timeout=3 # Tempo limite de comando
        )
        
        # Tenta um comando simples para verificar a conexão
        client.ping()
        logger.info("Conexão Redis estabelecida com sucesso.")
        redis_client = client
        return redis_client
    
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Erro ao conectar ao Redis em {REDIS_HOST}:{REDIS_PORT}. Caching indisponível. Detalhes: {e}")
        # Retorna None se a conexão falhar
        redis_client = False # Define como False para evitar tentativas repetidas em cada chamada
        return None

# Inicializa o cliente ao carregar o módulo
# A chamada é encapsulada em get_redis_client, o que garante a tentativa de conexão
# get_redis_client() 


def cache_url(short_code: str, original_url: str):
    """Armazena a URL original no Redis com um TTL."""
    client = get_redis_client()
    if client:
        try:
            client.setex(short_code, CACHE_TTL_SECONDS, original_url)
            logger.debug(f"Cache HIT para {short_code} armazenado no Redis.")
        except Exception as e:
            logger.error(f"Erro ao armazenar cache para {short_code}: {e}")

def get_cached_url(short_code: str) -> Optional[str]:
    """Busca a URL original no cache."""
    client = get_redis_client()
    if client:
        try:
            return client.get(short_code)
        except Exception as e:
            logger.error(f"Erro ao ler cache para {short_code}: {e}")
    return None

def invalidate_url_cache(short_code: str):
    """Invalida/deleta a entrada no cache."""
    client = get_redis_client()
    if client:
        try:
            client.delete(short_code)
            logger.debug(f"Cache para {short_code} invalidado.")
        except Exception as e:
            logger.error(f"Erro ao invalidar cache para {short_code}: {e}")