# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.core.database import get_db
# from app.schemas.url_schema import URLCreate, URLResponse
# from app.services.url_service import create_short_url, get_original_url, list_urls, delete_url
# from fastapi.responses import RedirectResponse

# router = APIRouter(tags=["URLs"])

# @router.post("/urls/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
# def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
#     return create_short_url(db, url_data)

# @router.get("/urls/", response_model=list[URLResponse])
# def get_all_urls(db: Session = Depends(get_db)):
#     return list_urls(db)

# @router.delete("/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
# def remove_url(short_code: str, db: Session = Depends(get_db)):
#     if not delete_url(db, short_code):
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")

# @router.get("/{short_code}", summary="Redireciona para a URL original")
# def redirect_url(short_code: str, db: Session = Depends(get_db)):
#     url = get_original_url(db, short_code)
#     if not url:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")
#     return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.url_schema import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_original_url, list_urls, delete_url
from fastapi.responses import RedirectResponse
from app.core.security import get_current_username # Importa a dependência de segurança atualizada

router = APIRouter(tags=["URLs"])

# Rotas que exigem autenticação
@router.post("/urls/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(
    url_data: URLCreate, 
    db: Session = Depends(get_db), 
    username: str = Depends(get_current_username) # Protegida com JWT
):
    """Cria uma URL curta. Requer autenticação."""
    return create_short_url(db, url_data)

@router.get("/urls/", response_model=list[URLResponse])
def get_all_urls(
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username) # Protegida com JWT
):
    """Lista todas as URLs curtas. Requer autenticação."""
    return list_urls(db)

@router.delete("/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def remove_url(
    short_code: str, 
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username) # Protegida com JWT
):
    """Deleta uma URL pelo código curto. Requer autenticação."""
    if not delete_url(db, short_code):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")

# Rota de redirecionamento (PÚBLICA)
@router.get("/{short_code}", summary="Redireciona para a URL original")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """Redireciona o usuário para a URL original. Rota pública."""
    url = get_original_url(db, short_code)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")
    # Retorna o status 307 (Temporary Redirect) para manter o método HTTP original, se for o caso
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)