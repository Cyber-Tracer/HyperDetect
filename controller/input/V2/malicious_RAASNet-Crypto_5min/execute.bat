@echo off
cd /d "%~dp0"

start "" payload_PyCrypto.exe

timeout /t 300 /nobreak > NUL

taskkill /IM "payload_PyCrypto.exe" /F
