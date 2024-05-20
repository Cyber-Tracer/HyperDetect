@echo off
cd /d "%~dp0"

start "" payload_PyAES.exe

timeout /t 1800 /nobreak > NUL

taskkill /IM "payload_PyAES.exe" /F

