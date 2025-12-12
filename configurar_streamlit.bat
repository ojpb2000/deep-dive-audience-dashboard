@echo off
echo Configurando Streamlit para saltar el prompt de email...
echo.

REM Crear directorio de configuracion si no existe
if not exist "%USERPROFILE%\.streamlit" mkdir "%USERPROFILE%\.streamlit"

REM Crear archivo de configuracion
echo [general] > "%USERPROFILE%\.streamlit\credentials.toml"
echo email = "" >> "%USERPROFILE%\.streamlit\credentials.toml"

echo [OK] Configuracion completada
echo.
echo Ahora puedes ejecutar EJECUTAR_AHORA.bat sin que pida email
pause

