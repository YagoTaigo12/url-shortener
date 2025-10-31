# 🚀 Encurtador de URLs – MVP

## 📦 Tecnologias
- Python 3.10+
- FastAPI
- MySQL 8
- SQLAlchemy
- Docker Compose
- Nginx
- Redis (futuro)

## ⚙️ Setup Local
```bash
docker-compose up --build
```
Acesse a API:
👉 http://localhost:8000/docs
---
## ✅ Resultado esperado ao rodar:
```bash
docker-compose up --build
```
Banco MySQL sobe com base url_shortener
FastAPI disponível em http://localhost:8000
Swagger docs em http://localhost:8000/docs
Nginx servindo como proxy reverso em http://localhost
