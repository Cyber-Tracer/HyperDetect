@echo off
cd /d "%~dp0"

start "" LibreOfficeDrawPortable.exe

timeout /t 300 /nobreak > NUL

taskkill /IM "soffice.bin" /F

