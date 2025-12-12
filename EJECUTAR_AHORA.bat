@echo off
chcp 65001 >nul
echo ========================================
echo Iniciando Hilton Deep Divers Dashboard
echo ========================================
echo.

cd /d "C:\Users\oscar.perez\OneDrive - OneWorkplace\Documentos\2025\Hilton\Hilton - Deep Divers"

echo Directorio actual:
cd
echo.

echo Verificando archivos...
if exist app.py (
    echo [OK] app.py encontrado
) else (
    echo [ERROR] app.py no encontrado
    echo Directorio actual:
    cd
    pause
    exit /b 1
)

if exist "Various_HIlton - Deep DiversvsNationally representative.csv" (
    echo [OK] CSV encontrado
) else (
    echo [ERROR] CSV no encontrado
    pause
    exit /b 1
)

echo.
echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python no encontrado en PATH
    echo Por favor, instala Python o agrega Python al PATH
    pause
    exit /b 1
) else (
    echo [OK] Python encontrado
    python --version
)

echo.
echo Verificando Streamlit...
python -m streamlit --version >nul 2>&1
if errorlevel 1 (
    echo [ADVERTENCIA] Streamlit no encontrado, instalando...
    python -m pip install streamlit pandas plotly numpy -q
)

echo.
echo ========================================
echo Iniciando Streamlit...
echo ========================================
echo.
echo IMPORTANTE: Si Streamlit pregunta por email, presiona Enter para continuar
echo.
echo El dashboard se abrira automaticamente en tu navegador.
echo Si no se abre, ve a: http://localhost:8080
echo.
echo Para detener el servidor, presiona Ctrl+C
echo.
echo ========================================
echo.

REM Configurar Streamlit para usar localhost y puerto 8080
python -m streamlit run app.py --server.port 8080 --server.address localhost

echo.
echo Dashboard cerrado.
pause

