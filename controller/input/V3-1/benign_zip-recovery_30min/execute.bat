REM Remove all files in the destination directory
del /q "C:\Users\Client\Documents\*.*"
REM Remove all subdirectories and their contents in the destination directory
for /d %%x in ("C:\Users\Client\Documents\*") do @rd /s /q "%%x"

REM Extract the zip file using PowerShell
powershell -command "Expand-Archive -Path 'D:\Documents_tst.zip' -DestinationPath 'C:\Users\Client\Documents' -Force"
del /q "D:\Documents_tst.zip"
