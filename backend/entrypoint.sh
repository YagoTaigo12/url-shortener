#!/bin/sh
# Aguarda o banco de dados MySQL antes de iniciar o app

set -e

echo " Aguardando banco de dados..."
RETRY=0
until python - <<'PY'
import os, sys
from sqlalchemy import create_engine

url = os.getenv("DATABASE_URL")
if not url:
    print("DATABASE_URL não definida.")
    sys.exit(1)

try:
    engine = create_engine(url)
    conn = engine.connect()
    conn.close()
except Exception as e:
    print("DB indisponível:", e)
    sys.exit(2)
PY
do
    RETRY=$((RETRY + 1))
    if [ $RETRY -gt 10 ]; then
        echo " Falha ao conectar ao DB após múltiplas tentativas."
        exit 1
    fi
    echo "Aguardando 5 segundos... ($RETRY/10)"
    sleep 5
done

echo " Banco de dados disponível! Iniciando aplicação..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
