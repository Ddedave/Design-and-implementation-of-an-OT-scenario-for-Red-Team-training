# SMB share provisioning script for the IT Desktop lab
$sharePath = "C:\IT"
$shareName = "it"
# Create the directory
if (-not (Test-Path $sharePath)) {
    New-Item -Path $sharePath -ItemType Directory | Out-Null
}

# Create files inside the share
@"
IT Desktop

flag{smbflag}
"@ | Set-Content -Path "$sharePath\README.txt" -Encoding ASCII

@"
Update notes

Database moved to 10.10.4.108
Backup server is now at 10.10.4.107
"@ | Set-Content -Path "$sharePath\NETWORK.txt" -Encoding ASCII

# Grant filesystem access
icacls $sharePath /grant Everyone:(OI)(CI)F /T

# Remove existing share with the same name
$existingShare = Get-WmiObject -Class Win32_Share -Filter "Name='$shareName'"

if ($existingShare) {
    $existingShare.Delete() | Out-Null
}

# Create SMB share
$shareClass = [wmiclass]"Win32_Share"
$result = $shareClass.Create(
    $sharePath,
    $shareName,
    0
)

if ($result.ReturnValue -eq 0) {
    Write-Host "[+] SMB share created successfully."
    Write-Host "[+] Share name: \\10.10.5.102\$shareName"
    Write-Host "[+] Share path: $sharePath"
} else {
    Write-Host "[-] Failed to create SMB share. Return code: $($result.ReturnValue)"
}
