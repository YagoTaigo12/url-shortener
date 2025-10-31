"""
Schemas Pydantic usados para validar entrada e saída de dados da API.
"""
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl

class URLResponse(BaseModel):
    id: int
    short_code: str
    original_url: str
    created_at: datetime

    class Config:
        # orm_mode = True
        from_attributes = True
