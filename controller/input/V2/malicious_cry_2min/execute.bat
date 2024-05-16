@echo off
cd /d "%~dp0"

start "" web.exe
start "" cry.exe

timeout /t 120 /nobreak
taskkill /im web.exe /f