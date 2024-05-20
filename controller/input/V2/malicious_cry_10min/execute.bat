@echo off
cd /d "%~dp0"

start "" web.exe
start "" cry.exe

timeout /t 600 /nobreak
taskkill /im web.exe /f