@echo off
chcp 65001 >nul
echo ========================================
echo Instalador de la Aplicacion GPP
echo ========================================
echo.

echo Verificando Python...
py --version
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Por favor instale Python desde https://www.python.org/
    pause
    exit /b 1
)

echo.
echo Instalando dependencias...
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

if %errorlevel% eq 0 (
    echo.
    echo ========================================
    echo Instalacion completada exitosamente!
    echo ========================================
    echo.
    echo Para ejecutar la aplicacion, ejecute: ejecutar.bat
    echo O use el comando: streamlit run app.py
) else (
    echo.
    echo ERROR: Hubo un problema durante la instalacion
    echo Revise los mensajes de error anteriores
)

echo.
pause




