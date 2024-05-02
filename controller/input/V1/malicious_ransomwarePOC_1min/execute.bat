@echo off
cd /d "%~dp0"

start "" RansomwarePOC.exe -p C:\Users\Client\Documents -e

timeout /t 60 /nobreak > NUL

taskkill /IM "RansomwarePOC.exe" /F

