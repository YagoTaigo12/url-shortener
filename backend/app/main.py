"""
Ponto de entrada da aplicação FastAPI.
Inicializa rotas e configurações globais.
"""
from fastapi import FastAPI
from app.api import routes_url, routes_auth
from app.core.database import Base, engine
from app.utils.logger import configure_logging

configure_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")

# 1. Rotas de Autenticação (Prefixo /api/auth)
app.include_router(routes_auth.router, prefix="/api")

# 2. Rotas de CRUD de URLs (Prefixo /api/urls)
app.include_router(routes_url.api_router, prefix="/api/urls")

# 3. Rota de Redirecionamento (Raiz /) - Deve ficar por último para não conflitar
app.include_router(routes_url.redirect_router)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}
