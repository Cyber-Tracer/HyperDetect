@echo off
cd /d "%~dp0"

start "" LibreOfficeCalcPortable.exe

timeout /t 60 /nobreak > NUL

taskkill /IM "soffice.bin" /F

