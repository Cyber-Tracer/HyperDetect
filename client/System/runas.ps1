param (
    [string]$CredentialPath,
    [string]$BatFilePath
)

# Import the credentials
$Credential = Import-Clixml -Path $CredentialPath
Start-Process cmd.exe "/c $BatFilePath" -Credential $Credential