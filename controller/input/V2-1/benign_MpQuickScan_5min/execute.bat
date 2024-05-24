@echo off
cd /d "%~dp0"
PowerShell -Command "Start-MpScan -ScanType QuickScan"
