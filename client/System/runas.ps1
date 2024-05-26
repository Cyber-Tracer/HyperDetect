param (
    [string]$CredentialPath,
    [string]$BatFilePath
)

# Import the credentials
$Credential = Import-Clixml -Path $CredentialPath
$dir = Split-Path -Path $BatFilePath
Start-Process "$BatFilePath" -Credential $Credential -LoadUserProfile -WorkingDirectory $dir