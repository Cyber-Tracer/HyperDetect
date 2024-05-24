@echo off
cd /d "%~dp0"

start "" roar.exe -e

timeout /t 6000 /nobreak > NUL

taskkill /IM "roar.exe" /F

