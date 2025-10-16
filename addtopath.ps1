# AddPythonScriptsPath.ps1
$ScriptsPath = "$env:APPDATA\Python\Python313\Scripts"

# Read current user PATH
$CurrentUserPath = [Environment]::GetEnvironmentVariable("Path", "User")

# Check if Scripts path is already in PATH
if ($CurrentUserPath -notlike "*$ScriptsPath*") {
    # Append Scripts folder
    $NewUserPath = $CurrentUserPath + ";" + $ScriptsPath

    # Update the user PATH
    [Environment]::SetEnvironmentVariable("Path", $NewUserPath, "User")
    Write-Host "[SUCCESS] Added $ScriptsPath to User PATH."
    Write-Host "⚠️ Restart your terminal or VS Code to use 'pico'."
} else {
    Write-Host "[INFO] Scripts folder already in PATH."
}
