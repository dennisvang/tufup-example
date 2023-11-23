# DISCLAIMER:
# This script automatically creates files on your system, related to the example
# "my_app", and deletes them afterwards. Confirmation is requested before deleting.
# Use at your own risk.
#
# This script executes the steps from the README, both for the repo-side and the
# client-side. This is basically the same as the test-update-cycle.yml github workflow,
# except you run this on your local development system, for convenient manual testing.
#
# - initialize a new example repository in a .\temp_my_app dir (including dummy keystore)
# - create my_app v1.0 bundle using pyinstaller
# - add my_app v1.0 to tufup repository
# - install my_app v1.0 in <localappdata>\Programs\my_app with data in <localappdata>\my_app
# - mock develop my_app v2.0
# - create my_app v2.0 bundle using pyinstaller
# - add my_app v2.0 to tufup repository
# - run update server and update my_app from v1 to v2
#
# if the script won't execute, run the following command:
#   `Set-ExecutionPolicy AllSigned`
# https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scripts
#
# note we could simply run this script in the github workflow,
# but workflow failures are easier to debug when broken down into
# separate steps

$app_name = "my_app"
$enable_patch_update = $true

# directories where this script creates files and deletes files (note these must end
# with $app_name and must be consistent with myapp.settings and repo_settings)
$repo_dir = $PSScriptRoot
$temp_dir = "$repo_dir\temp_$app_name"
$app_install_dir = "$env:LOCALAPPDATA\Programs\$app_name"
$app_data_dir = "$env:LOCALAPPDATA\$app_name"
$targets_dir = "$app_data_dir\update_cache\targets"
$all_app_dirs = @($temp_dir, $app_install_dir, $app_data_dir)

function Remove-MyAppDirectory {
    # remove a *my_app directory after confirmation
    param($Path)
    if ( $Path -match "$app_name$" ) {
        if (Test-Path $Path) {
            # I think recurse can be used here, despite "known issues"...
            Remove-Item $Path -Recurse -Confirm
        } else {
            Write-Host "path does not exist: $Path" -ForegroundColor yellow
        }
    } else {
        Write-Host "$app_name not in path: $Path" -ForegroundColor yellow
    }
}

function Remove-MyApp {
    $all_app_dirs | ForEach-Object { Remove-MyAppDirectory $_ }
}

# remove leftover directories and files, if any
Remove-MyApp

# create directories if they do not exist yet
$all_app_dirs | ForEach-Object {
    if (!(Test-Path $_)) {
        New-Item -Path $_ -ItemType "directory" | Out-Null
        Write-Host "directory created: $_" -ForegroundColor green
    }
}
New-Item -Path $targets_dir -ItemType "directory" -Force | Out-Null

# this script requires an active python environment, with tufup installed
# (we'll assume there's a venv in the repo_dir)
$venv_path = "$repo_dir\venv\Scripts\activate.ps1"
if (Test-Path $venv_path) {
    & $venv_path
    Write-Host "venv activated" -ForegroundColor green
} else {
    Write-Host "venv not found" -ForegroundColor red
}

# make sure python can find myapp
$Env:PYTHONPATH += ";$repo_dir\src"

# - initialize new repository
Write-Host "initializing tuf repository for myapp" -ForegroundColor green
python "$repo_dir\repo_init.py"

# - create my_app v1.0 bundle using pyinstaller
Write-Host "creating myapp v1.0 bundle" -ForegroundColor green
Push-Location $repo_dir
& "$repo_dir\create_pyinstaller_bundle_win.bat"
Pop-Location

# - add my_app v1.0 to tufup repository
Write-Host "adding myapp v1.0 bundle to repo" -ForegroundColor green
python "$repo_dir\repo_add_bundle.py"

# - mock install my_app v1.0
$myapp_v1_archive = "$temp_dir\repository\targets\$app_name-1.0.tar.gz"
tar -xf $myapp_v1_archive --directory=$app_install_dir
# put a copy of the archive in the targets dir, to enable patch updates
if ($enable_patch_update) {
    Write-Host "enabling patch update" -ForegroundColor green
    Copy-Item $myapp_v1_archive -Destination $targets_dir
}

# - mock develop my_app v2.0
# (quick and dirty, this modifies the actual source,
# but the change is rolled back later...)
Write-Host "bumping myapp version to v2.0" -ForegroundColor green
$settings_path = "$repo_dir\src\myapp\settings.py"
(Get-Content $settings_path).Replace("1.0", "2.0") | Set-Content $settings_path

# - create my_app v2.0 bundle using pyinstaller
Write-Host "creating myapp v2.0 bundle" -ForegroundColor green
Push-Location $repo_dir
& "$repo_dir\create_pyinstaller_bundle_win.bat"
Pop-Location

# - add my_app v2.0 to tufup repository
Write-Host "adding myapp v2.0 bundle to repo" -ForegroundColor green
python "$repo_dir\repo_add_bundle.py"

# - roll-back modified source
(Get-Content $settings_path).Replace("2.0", "1.0") | Set-Content $settings_path

# - start update server
Write-Host "starting update server" -ForegroundColor green
$job = Start-Job -ArgumentList @("$temp_dir\repository") -ScriptBlock {
    param($repository_path)
    python -m http.server -d $repository_path
}
sleep 1  # not sure if this is required, but cannot hurt

# - run my_app to update from v1 to v2
Write-Host "running $app_name for update..." -ForegroundColor green
Invoke-Expression "$app_install_dir\main.exe"

# - run my_app again to verify we now have v2.0
Write-Host "hit enter to proceed, after console has closed:"  -ForegroundColor yellow -NoNewLine
Read-Host  # no text: we use write host to add color
Write-Host "running $app_name again to verify version" -ForegroundColor green
$output = Invoke-Expression "$app_install_dir\main.exe"

# - stop update server
Write-Host "stopping server" -ForegroundColor green
$job | Stop-Job

# - test output
$pattern = "$app_name 2.0"
if ( $output -match $pattern ) {
  Write-Host "`nSUCCESS: $pattern found" -ForegroundColor green
} else {
  Write-Host "`nFAIL: $pattern not found in:`n$output" -ForegroundColor red
  exit 1
}

# reminder to clean up
$remaining = 0
$all_app_dirs | ForEach-Object {
    if (Test-Path $_) {
        Write-Host "$app_name files remain in: $_" -ForegroundColor yellow
        $remaining += 1
    }
}
if ($remaining) {
    Write-Host "Would you like to remove these directories?" -ForegroundColor yellow
    if ((Read-Host "[y]/n") -in "", "y") {
        Remove-MyApp
    }
}
