@echo off
REM GIESTA Bot v2.7 - Quick Start Script (Windows)

echo.
echo ========================================
echo   GIESTA BOT v2.7 - QUICK START
echo ========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale Python 3.10+ de:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Verificar se .env existe
if not exist .env (
    echo [AVISO] Arquivo .env nao encontrado!
    echo.
    echo Copiando .env.example para .env...
    copy .env.example .env >nul
    echo.
    echo [ACAO NECESSARIA]
    echo Por favor, edite o arquivo .env e adicione:
    echo   - TELEGRAM_TOKEN (do @BotFather)
    echo   - CHAT_ID (do @userinfobot)
    echo.
    echo Pressione qualquer tecla para abrir o .env...
    pause >nul
    notepad .env
    echo.
)

REM Verificar se requirements estão instalados
echo Verificando dependencias...
pip show python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INSTALACAO] Instalando dependencias...
    echo Isso pode levar 1-2 minutos...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar dependencias
        echo Tente manualmente: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependencias instaladas
)

echo [OK] Dependencias verificadas
echo.

REM Perguntar se quer testar APIs
echo.
echo Deseja testar as APIs antes de iniciar? (s/n)
set /p teste=">> "

if /i "%teste%"=="s" (
    echo.
    echo [TESTE] Executando test_apis.py...
    echo.
    python test_apis.py
    echo.
    echo.
    echo Pressione qualquer tecla para continuar...
    pause >nul
)

echo.
echo ========================================
echo   INICIANDO GIESTA BOT...
echo ========================================
echo.
echo O bot vai rodar aqui neste terminal.
echo NAO FECHE esta janela!
echo.
echo No Telegram:
echo   1. Procure seu bot
echo   2. Envie: /start
echo.
echo Pressione Ctrl+C para parar o bot.
echo.
echo ----------------------------------------
echo.

REM Iniciar o bot
python bot.py

echo.
echo ========================================
echo   BOT ENCERRADO
echo ========================================
echo.
pause
