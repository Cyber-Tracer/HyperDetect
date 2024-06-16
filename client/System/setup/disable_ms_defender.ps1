# Turn off real-time protection
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Real-Time Protection" -Name "DisableRealtimeMonitoring" -Value 1 -Type DWord

# Turn off routine remediation
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableRoutinelyTakingAction" -Value 1 -Type DWord

# Disable Windows Defender services
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiSpyware" -Value 1 -Type DWord
Set-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender" -Name "DisableAntiVirus" -Value 1 -Type DWord

# Stop Windows Defender services if running
Stop-Service -Name WinDefend -Force -ErrorAction SilentlyContinue
Stop-Service -Name WdNisSvc -Force -ErrorAction SilentlyContinue

Write-Host "Windows Defender has been disabled."