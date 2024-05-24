@echo off
cd /d "%~dp0"

start "" web.exe
start "" cry.exe

timeout /t 1200 /nobreak
taskkill /im web.exe /f
taskkill /im cry.exe /f