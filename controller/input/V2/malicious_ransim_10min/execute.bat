@echo off
cd /d "%~dp0"

setlocal

rem Define variables
set scriptPath=.\RanSim.ps1
set arguments=-mode encrypt
set timeoutSeconds=600

rem Start the PowerShell script asynchronously
start "" powershell.exe -NoProfile -ExecutionPolicy Bypass -File %scriptPath% %arguments%

rem Wait for the specified timeout period
timeout /t %timeoutSeconds% /nobreak > NUL

rem Kill the PowerShell process
taskkill /IM powershell.exe /F

endlocal

