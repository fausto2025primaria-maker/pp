@echo off
chcp 65001 >nul
echo Generant cataleg del Portal Far...
python scripts\generar_portal.py
echo.
echo Fet. Revisa data\apps.json i puja els canvis a GitHub.
pause
