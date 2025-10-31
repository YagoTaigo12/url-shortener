"""
Define as rotas principais da API relacionadas ao encurtamento de URLs.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.url_schema import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_original_url

router = APIRouter(prefix="/urls", tags=["URLs"])

@router.post("/", response_model=URLResponse)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    """Endpoint para encurtar uma nova URL."""
    new_url = create_short_url(db, url_data)
    return new_url

@router.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    """Endpoint para redirecionar uma URL encurtada."""
    url = get_original_url(db, short_code)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    # Em uma implementação real, faríamos um RedirectResponse aqui
    return {"original_url": url.original_url}
