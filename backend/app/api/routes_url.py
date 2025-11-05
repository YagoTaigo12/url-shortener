from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.url_schema import URLCreate, URLResponse
from app.services.url_service import create_short_url, get_original_url, list_urls, delete_url
from fastapi.responses import RedirectResponse

router = APIRouter(tags=["URLs"])

@router.post("/urls/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(url_data: URLCreate, db: Session = Depends(get_db)):
    return create_short_url(db, url_data)

@router.get("/urls/", response_model=list[URLResponse])
def get_all_urls(db: Session = Depends(get_db)):
    return list_urls(db)

@router.delete("/urls/{short_code}", status_code=status.HTTP_204_NO_CONTENT)
def remove_url(short_code: str, db: Session = Depends(get_db)):
    if not delete_url(db, short_code):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")

@router.get("/{short_code}", summary="Redireciona para a URL original")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    url = get_original_url(db, short_code)
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="URL não encontrada")
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
