@echo off
cd /d "%~dp0"
echo Starting incoming invoices...
start "Vlezni fakturi" python app.py
timeout /t 2 /nobreak >nul
start http://localhost:5050
