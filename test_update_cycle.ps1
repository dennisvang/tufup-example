# if the script won't execute, run the following command:
#   `Set-ExecutionPolicy AllSigned`
# https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scripts

# remove content of temp dir
$repo_dir = $PSScriptRoot
$temp_dir = "$repo_dir\temp"
$abort = Read-Host "This will delete everything from '$temp_dir'`nHit enter to continue, or any other key to abort"
if ( $abort ) {
    Write-Output "aborted"
    exit
}
# we could simply remove $tempdir\*, but let's just be a bit more specific
# to prevent accidental deletion of unrelated files
# https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-arrays
$subdirs = $("build", "dist", "keystore", "repository")
# I think recurse can be used here, despite "known issues"...
$subdirs | ForEach-Object {
    $path = "$temp_dir\$_"
    if (Test-Path $path) {
        Remove-Item $path -Recurse  # -Confirm
        Write-Output "removed '$path'"
    }
}
