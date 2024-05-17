@echo off
cd /d "%~dp0"

PowerShell ".\RanSim.ps1 -mode encrypt"

taskkill /IM "powershell.exe" /F

