param(
    [string]$username
)

$user = Get-WmiObject -Class Win32_UserAccount -Filter "Name = '$username'"
$fullUserName = "$($user.Domain)\$($user.Name)"

# Define the task name and the action
$taskName = "\Start Logging"
$action = New-ScheduledTaskAction -Execute "C:\HyperDbg\client\start_logging.bat"

# Define the trigger (logon trigger)
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $fullUserName

# Define the principal with the highest run level
$principal = New-ScheduledTaskPrincipal -UserId $user.SID -LogonType Interactive -RunLevel Highest

# Define the settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable:$false -RunOnlyIfNetworkAvailable:$false `
                -Hidden:$false

# Create the scheduled task
$task = New-ScheduledTask -Action $action -Principal $principal -Trigger $trigger -Settings $settings

# Register the scheduled task
Register-ScheduledTask -TaskName $taskName -InputObject $task -User $fullUserName

