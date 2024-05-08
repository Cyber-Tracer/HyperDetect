@echo off
cd /d "%~dp0"

msiexec /i LibreOffice_24.2.3_Win_x86-64.msi /quiet /norestart ALLUSERS=1

timeout /t 10

msiexec /x LibreOffice_24.2.3_Win_x86-64.msi /quiet /norestart ALLUSERS=1

