@echo off
cd /d "%~dp0"

start "" LibreOfficeDrawPortable.exe

timeout /t 60 /nobreak > NUL

taskkill /IM "soffice.bin" /F

