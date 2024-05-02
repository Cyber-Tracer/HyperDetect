# Define the source directory, destination zip file, and timeout in seconds
$sourcePath = "C:\Users\Client\Documents\Archive.zip"
$currentLocation = Get-Location
$destinationDir = "output"
$destinationDir = Join-Path -Path $currentLocation -ChildPath $destinationDir
$timeoutSeconds = 60  # Set the timeout

# Start a job to run the compression
$job = Start-Job -ScriptBlock {
    param($sourcePath, $destinationDir)
    powershell -Command "Expand-Archive -Path $sourcePath -DestinationPath $destinationDir"
} -ArgumentList $sourcePath, $destinationDir

# Wait for the job to complete with a timeout
if (Wait-Job -Job $job -Timeout $timeoutSeconds) {
    # If job completed within timeout, receive job output (if any)
    Receive-Job -Job $job
    Write-Output "Compression completed successfully."
    Remove-Job -Job $job
} else {
    # If job did not complete, stop the job and write timeout message
    Stop-Job -Job $job
    Remove-Job -Job $job
    Write-Error "Compression timed out after $timeoutSeconds seconds."
}

