@echo off
cd /d "%~dp0"
"C:\Program Files\7-zip\7z.exe" x lockbit.zip -pinfected
lockbit.exe