param (
    [string]$CredentialPath
)

$Credential = Get-Credential
$Credential | Export-Clixml -Path $CredentialPath