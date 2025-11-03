#!/bin/bash
# GIESTA Bot v2.7 - Quick Start Script (Linux/Mac)

echo ""
echo "========================================"
echo "  GIESTA BOT v2.7 - QUICK START"
echo "========================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERRO] Python3 não encontrado!"
    echo ""
    echo "Por favor, instale Python 3.10+ de:"
    echo "  Mac: brew install python3"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo ""
    exit 1
fi

echo "[OK] Python encontrado: $(python3 --version)"
echo ""

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "[AVISO] Arquivo .env não encontrado!"
    echo ""
    echo "Copiando .env.example para .env..."
    cp .env.example .env
    echo ""
    echo "[AÇÃO NECESSÁRIA]"
    echo "Por favor, edite o arquivo .env e adicione:"
    echo "  - TELEGRAM_TOKEN (do @BotFather)"
    echo "  - CHAT_ID (do @userinfobot)"
    echo ""
    echo "Pressione ENTER para abrir o .env..."
    read -r
    ${EDITOR:-nano} .env
    echo ""
fi

# Verificar se requirements estão instalados
echo "Verificando dependências..."
if ! python3 -c "import telegram" &> /dev/null; then
    echo ""
    echo "[INSTALAÇÃO] Instalando dependências..."
    echo "Isso pode levar 1-2 minutos..."
    echo ""
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "[ERRO] Falha ao instalar dependências"
        echo "Tente manualmente: pip3 install -r requirements.txt"
        echo ""
        exit 1
    fi
    echo ""
    echo "[OK] Dependências instaladas"
fi

echo "[OK] Dependências verificadas"
echo ""

# Perguntar se quer testar APIs
echo ""
echo "Deseja testar as APIs antes de iniciar? (s/n)"
read -p ">> " teste

if [ "$teste" = "s" ] || [ "$teste" = "S" ]; then
    echo ""
    echo "[TESTE] Executando test_apis.py..."
    echo ""
    python3 test_apis.py
    echo ""
    echo ""
    echo "Pressione ENTER para continuar..."
    read -r
fi

echo ""
echo "========================================"
echo "  INICIANDO GIESTA BOT..."
echo "========================================"
echo ""
echo "O bot vai rodar aqui neste terminal."
echo "NÃO FECHE esta janela!"
echo ""
echo "No Telegram:"
echo "  1. Procure seu bot"
echo "  2. Envie: /start"
echo ""
echo "Pressione Ctrl+C para parar o bot."
echo ""
echo "----------------------------------------"
echo ""

# Iniciar o bot
python3 bot.py

echo ""
echo "========================================"
echo "  BOT ENCERRADO"
echo "========================================"
echo ""
