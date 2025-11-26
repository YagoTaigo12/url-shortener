from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.url_schema import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_original_url, list_urls, delete_url
from fastapi.responses import RedirectResponse
from app.core.security import get_current_username
from app.core.redis_client import cache_url, invalidate_url_cache 

# Router para API (CRUD) - Será prefixado com /api/urls no main.py
api_router = APIRouter(tags=["URLs"])

# Router para Redirecionamento (Public) - Será montado na raiz / no main.py
redirect_router = APIRouter(tags=["Redirect"])

# --- API CRUD ---

@api_router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(
    url_data: URLCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    username: str = Depends(get_current_username)
):
    """Cria uma URL curta. Requer autenticação."""
    new_url = create_short_url(db, url_data)
    background_tasks.add_task(cache_url, new_url.short_code, new_url.original_url)
    return new_url

@api_router.get("/", response_model=list[URLResponse])
def get_all_urls(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username)
):
    """Lista todas as URLs curtas. Requer autenticação."""
    return list_urls(db)

@api_router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def remove_url(
    short_code: str, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username)
):
    """Deleta uma URL pelo código curto. Requer autenticação."""
    if not delete_url(db, short_code):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")
    background_tasks.add_task(invalidate_url_cache, short_code)

# --- REDIRECIONAMENTO PÚBLICO ---

@redirect_router.get("/{short_code}", summary="Redireciona para a URL original")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redireciona o usuário para a URL original. 
    A lógica de serviço agora prioriza o cache Redis. Rota pública na raiz.
    """
    url = get_original_url(db, short_code)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")
        
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
