@echo off
cd C:\HyperDbg\hyperdbg\release
runas /trustlevel:0x20000 "cmd /c C:\HyperDbg\client\execute.bat"
.\hyperdbg-cli.exe --script C:\HyperDbg\client\logger.ds
pause