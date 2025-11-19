"""
Ponto de entrada da aplicação FastAPI.
Inicializa rotas e configurações globais.
"""
from fastapi import FastAPI
from app.api import routes_url, routes_auth # Importa o novo router
from app.core.database import Base, engine
from app.utils.logger import configure_logging # Importa o logger

# Configura o logger antes de tudo
configure_logging()

# Cria as tabelas no banco se não existirem (agora inclui a tabela users)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

# Inclui as rotas
app.include_router(routes_auth.router) # Rotas de Autenticação
app.include_router(routes_url.router) # Rotas de URLs (agora protegidas)


@app.get("/")
def root():
    return {"message": "API do Encurtador de URLs está rodando 🚀"}