@echo off

cd /d "%~dp0"

set "source=C:\Users\Client\Documents\Archive"
set "target=output\"

xcopy "%source%\*.pdf" "%target%" /S /D /Y

echo PDF files have been copied from the source and its subdirectories.
pause
