FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./

# Instalação das dependências de compilação (necessárias para 'cryptography')
RUN apt-get update && \
    apt-get install -y build-essential libssl-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    # Limpeza para reduzir o tamanho da imagem final
    apt-get purge -y --auto-remove build-essential libssl-dev libffi-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
CMD ["/bin/sh", "/app/entrypoint.sh"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]