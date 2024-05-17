@echo off
cd /d "%~dp0"

start "" roar.exe -e

timeout /t 600 /nobreak > NUL

taskkill /IM "roar.exe" /F

