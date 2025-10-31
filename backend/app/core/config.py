"""
Arquivo de configuração geral do projeto.
Lê variáveis de ambiente e prepara constantes globais.
"""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REDIS_HOST: str
    REDIS_PORT: int
    LDAP_SERVER: str

    class Config:
        env_file = ".env"

settings = Settings()
