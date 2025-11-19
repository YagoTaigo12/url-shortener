#!/bin/bash
# Script para gerar certificados SSL auto-assinados na pasta do host 
# (nginx/certs) para uso no Docker Compose.

CERT_DIR="./certs"
KEY_FILE="$CERT_DIR/localhost.key"
CRT_FILE="$CERT_DIR/localhost.crt"
# Formato correto com a barra inicial
SUBJECT='/C=BR/ST=SP/L=Sao Paulo/O=URL Shortener Dev/CN=localhost'

echo "========================================================="
echo "  🚀 Preparando ambiente para Nginx e HTTPS (Sprint 5) 🔒"
echo "========================================================="

# 1. Cria a pasta para certificados se não existir
mkdir -p "$CERT_DIR"
echo "Pasta de certificados criada em: $CERT_DIR"

# 2. Verifica e gera os certificados se não existirem
if [ ! -f "$KEY_FILE" ] || [ ! -f "$CRT_FILE" ]; then
    echo "Gerando certificados SSL auto-assinados (localhost.crt, localhost.key)..."
    
    # Geração dos certificados usando openssl
    # SOLUÇÃO PARA GIT BASH (Windows): Desativa a conversão de caminhos
    MSYS_NO_PATHCONV=1 openssl req -x509 -nodes -days 365 \
        -newkey rsa:2048 \
        -keyout "$KEY_FILE" \
        -out "$CRT_FILE" \
        -subj "$SUBJECT"
    
    # Verifica o status de saída do openssl (se $? for 0, funcionou)
    if [ $? -eq 0 ]; then
        echo "✅ Certificados gerados com sucesso."
        # 3. Garante que as permissões estejam corretas APÓS a geração
        chmod 600 "$KEY_FILE" "$CRT_FILE"
        echo "Permissões de arquivos ajustadas."
    else
        echo "❌ ERRO: Falha ao gerar certificados com openssl."
        # Se falhar, o chmod não é executado no arquivo ausente.
    fi

    echo "Lembrete: Como são auto-assinados, o navegador pode exigir que você aceite o aviso de segurança."
else
    echo "Certificados já existem. Pulando a geração."
    # Garante que as permissões estejam corretas mesmo pulando a geração
    chmod 600 "$KEY_FILE" "$CRT_FILE"
    echo "Permissões de arquivos existentes verificadas/ajustadas."
fi

echo "Setup de certificados concluído. Agora você pode executar o 'docker-compose up -d'."