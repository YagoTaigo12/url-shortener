from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.url_schema import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_original_url, list_urls, delete_url
from app.services.auth_service import get_user_by_username
from fastapi.responses import RedirectResponse
from app.core.security import get_current_username
from app.core.redis_client import cache_url, invalidate_url_cache 

# Router para API (CRUD)
api_router = APIRouter(tags=["URLs"])

# Router para Redirecionamento (Public)
redirect_router = APIRouter(tags=["Redirect"])

# --- Helper para obter objeto User completo ---
def get_current_user_obj(db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    user = get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return user

# --- API CRUD ---

@api_router.post("/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(
    url_data: URLCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user_obj) # Injeta o objeto User
):
    """Cria uma URL curta vinculada ao usuário autenticado."""
    # Passamos o ID do usuário para o serviço
    new_url = create_short_url(db, url_data, user_id=current_user.id)
    
    # Cache em background
    background_tasks.add_task(cache_url, new_url.short_code, new_url.original_url)
    return new_url

@api_router.get("/", response_model=list[URLResponse])
def get_all_urls(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_obj) # Injeta o objeto User
):
    """Lista todas as URLs criadas apenas pelo usuário autenticado."""
    return list_urls(db, user_id=current_user.id)

@api_router.delete("/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def remove_url(
    short_code: str, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_obj) # Injeta o objeto User
):
    """Deleta uma URL se ela pertencer ao usuário autenticado."""
    success = delete_url(db, short_code, user_id=current_user.id)
    
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada ou permissão negada")
    
    background_tasks.add_task(invalidate_url_cache, short_code)

# --- REDIRECIONAMENTO PÚBLICO ---

@redirect_router.get("/{short_code}", summary="Redireciona para a URL original")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """
    Redireciona o usuário para a URL original. 
    Rota pública: não exige autenticação, qualquer um pode acessar o link curto.
    """
    url = get_original_url(db, short_code)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")
        
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)