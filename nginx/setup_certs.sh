#!/bin/bash
# Script para gerar certificados SSL auto-assinados na pasta do host 
# (nginx/certs) para uso no Docker Compose.

CERT_DIR="./certs"
KEY_FILE="$CERT_DIR/shrt.cc.key"
CRT_FILE="$CERT_DIR/shrt.cc.crt"
SUBJECT='/C=BR/ST=SP/L=Sao Paulo/O=URL Shortener Dev/CN=shrt.cc'

echo "========================================================="
echo "  🚀 Gerando certificados SSL para o domínio fake 🔒"
echo "========================================================="

mkdir -p "$CERT_DIR"

if [ ! -f "$KEY_FILE" ] || [ ! -f "$CRT_FILE" ]; then
    echo "Gerando certificados SSL auto-assinados (shrt.cc)..."

    MSYS_NO_PATHCONV=1 openssl req -x509 -nodes -days 365 \
        -newkey rsa:2048 \
        -keyout "$KEY_FILE" \
        -out "$CRT_FILE" \
        -subj "$SUBJECT"

    if [ $? -eq 0 ]; then
        echo "✅ Certificados gerados com sucesso."
        chmod 600 "$KEY_FILE" "$CRT_FILE"
    else
        echo "❌ ERRO: Falha ao gerar certificados."
    fi
else
    echo "Certificados já existem. Pulando a geração."
    chmod 600 "$KEY_FILE" "$CRT_FILE"
fi

echo "Certificados prontos!"
