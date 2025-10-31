"""
Ponto de entrada da aplicação FastAPI.
Inicializa rotas e configurações globais.
"""
from fastapi import FastAPI
from app.api import routes_url
from app.core.database import Base, engine

# Cria as tabelas no banco se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

# Inclui as rotas de URLs
app.include_router(routes_url.router)

@app.get("/")
def root():
    return {"message": "API do Encurtador de URLs está rodando 🚀"}
