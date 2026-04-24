@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║         📊 APLICACIÓN GPP - VERSIÓN PREMIUM 2025 📊           ║
echo ║                                                                ║
echo ║          Sistema de Evaluación de Gestión Por Procesos        ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo.
echo ✨ MEJORAS GRÁFICAS IMPLEMENTADAS:
echo.
echo    ✅ Paleta de colores premium moderna
echo    ✅ Gráficos optimizados y atractivos
echo    ✅ Animaciones suaves y profesionales
echo    ✅ Efectos glassmorphism en cards
echo    ✅ Tipografías premium (Outfit, Montserrat, Roboto)
echo    ✅ Dashboard profesional
echo.
echo ════════════════════════════════════════════════════════════════
echo.
echo 🚀 Iniciando la aplicación...
echo.
echo    Por favor espere mientras se carga Streamlit...
echo.
echo ════════════════════════════════════════════════════════════════
echo.

REM Activar el entorno virtual si existe
if exist "venv\Scripts\activate.bat" (
    echo 📦 Activando entorno virtual...
    call venv\Scripts\activate.bat
)

REM Ejecutar la aplicación de Streamlit
echo.
echo 🌐 Abriendo aplicación en el navegador...
echo.
streamlit run app.py

pause



