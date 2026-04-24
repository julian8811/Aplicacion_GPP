@echo off
chcp 65001 >nul
cls
echo ========================================
echo Iniciando Aplicacion de Evaluacion GPP
echo ========================================
echo.
echo La aplicacion se abrira en su navegador...
echo URL: http://localhost:8501
echo.
echo Para detener la aplicacion, presione Ctrl+C
echo.
echo ========================================
echo.

streamlit run app.py

pause


