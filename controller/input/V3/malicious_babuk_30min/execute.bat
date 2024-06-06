@echo off
REM https://bazaar.abuse.ch/sample/01c647838c374e91e8f9fe967fd25235d72264414bb0d5b82c4fbd4151a9717f/
cd /d "%~dp0"
"C:\Program Files\7-zip\7z.exe" x babuk.zip -pinfected
babuk.exe