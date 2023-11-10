# performs the steps from the README, basically the same as the
# test-update-cycle.yml github workflow, but locally:
#
# - initializes a new example repository in .\temp dir, including key pairs
# - create my_app v1.0 bundle using pyinstaller
# - add my_app v1.0 to tufup repository
# - mock install my_app v1.0
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

# remove content of temp dir
$repo_dir = $PSScriptRoot
$temp_dir = "$repo_dir\temp"
if (Test-Path $temp_dir) {
    $abort = Read-Host "This will delete everything from '$temp_dir'`nHit enter to continue, or any other key to abort"
    if ( $abort ) {
        Write-Host "aborted" -ForegroundColor red
        exit
    }
} else {
    New-Item -Path $temp_dir -ItemType "directory" | Out-Null
    Write-Host "temp dir created" -ForegroundColor green
}

# we could simply remove $tempdir\*, but let's just be a bit more specific
# to prevent accidental deletion of unrelated files
# https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-arrays
$subdirs = $("build", "dist", "keystore", "repository")
$subdirs | ForEach-Object {
    $path = "$temp_dir\$_"
    if (Test-Path $path) {
        # I think recurse can be used here, despite "known issues"...
        Remove-Item $path -Recurse  # -Confirm
        Write-Host "removed '$path'" -ForegroundColor green
    }
}

# remove any leftovers from localappdata (paths must match myapp.settings)
$app_install_dir = "$env:LOCALAPPDATA\Programs\my_app"
$app_data_dir = "$env:LOCALAPPDATA\my_app"
$($app_data_dir, $app_install_dir) | ForEach-Object {
    if (Test-Path $_) {
        Remove-Item "$_\*" -Confirm
    } else {
        New-Item -Path $_ -ItemType "directory" | Out-Null
        Write-Host "created dir $_" -ForegroundColor green
    }
}

# this script requires an active python environment with tufup installed
# we'll assume there's a venv in the repo_dir
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
$myapp_v1_archive = "$temp_dir\repository\targets\my_app-1.0.tar.gz"
tar -xf $myapp_v1_archive --directory=$app_install_dir
Write-Host "my_app v1.0 installed in $app_install_dir" -ForegroundColor green

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
$repository_path = "$temp_dir\repository"
if (!(Test-Path $repository_path)) {
    Write-Host "$repository_path not found" -ForegroundColor red
}
$job = Start-Job -ScriptBlock {
    python -m http.server -d $repository_path
}
sleep 1
# todo: server appears unreachable... is it running?
#curl -Uri "http://localhost:8000/metadata/timestamp.json"

# - run my_app to update from v1 to v2
Write-Host "running my_app for update..." -ForegroundColor green
Invoke-Expression "$app_install_dir\main.exe"

# - run my_app again to verify we now have v2.0
Write-Host "running my_app again to verify version" -ForegroundColor green
$output = Invoke-Expression "$app_install_dir\main.exe"

# - stop update server
Write-Host "stopping server" -ForegroundColor green
$job | Stop-Job
