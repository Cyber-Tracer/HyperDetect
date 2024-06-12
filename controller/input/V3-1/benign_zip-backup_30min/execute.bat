@echo off
cd /d "%~dp0"
powershell -command "Compress-Archive -Path 'C:\Users\Client\Documents\*' -DestinationPath 'D:\FileBackup\Documents_tst.zip'"