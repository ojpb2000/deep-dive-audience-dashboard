@echo off
echo ========================================
echo  Subir Proyecto a GitHub
echo ========================================
echo.

REM Verificar si git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git no está instalado o no está en el PATH
    echo Por favor instala Git desde: https://git-scm.com/downloads
    pause
    exit /b 1
)

echo [1/5] Inicializando Git...
git init

echo.
echo [2/5] Agregando remote de GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/ojpb2000/deep-divers-yougov.git

echo.
echo [3/5] Agregando archivos...
git add .

echo.
echo [4/5] Haciendo commit inicial...
git commit -m "Initial commit: Hilton Deep Divers Dashboard with AI Insights"

echo.
echo [5/5] Subiendo a GitHub...
echo.
echo NOTA: Si te pide credenciales:
echo - Username: tu_usuario_de_github
echo - Password: usa un Personal Access Token (NO tu contraseña)
echo.
echo Para crear un token:
echo 1. GitHub -^> Settings -^> Developer settings -^> Personal access tokens
echo 2. Generate new token (classic)
echo 3. Selecciona permisos: repo
echo 4. Copia el token y úsalo como password
echo.

git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo subir. Verifica:
    echo 1. Que el repositorio existe en GitHub
    echo 2. Que tienes permisos para escribir
    echo 3. Que usaste un Personal Access Token como password
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo  ¡Proyecto subido exitosamente!
echo ========================================
echo.
echo Repositorio: https://github.com/ojpb2000/deep-divers-yougov
echo.
echo Siguiente paso: Deploy en Streamlit Community Cloud
echo https://share.streamlit.io
echo.
pause

