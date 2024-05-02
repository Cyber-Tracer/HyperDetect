@echo off
cd /d "%~dp0"

start "" LibreOfficeWriterPortable.exe

timeout /t 60 /nobreak > NUL

taskkill /IM "soffice.bin" /F

