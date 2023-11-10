# if the script won't execute, run the following command:
#   `Set-ExecutionPolicy AllSigned`
# https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_scripts

# remove content of temp dir
$tempdir = "$PSScriptRoot\temp"
$abort = Read-Host "This will delete everything from '$tempdir'`nHit enter to continue, or any other key to abort"
if ( $abort ) {
    Write-Output "aborted"
    exit
}
# we could simply remove $tempdir\*, but let's just be a bit more specific
# to prevent accidental deletion of unrelated files
# https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-arrays
$subdirs = $("aap") # $("build", "dist", "keystore", "repository")
# I think recurse can be used here, despite "known issues"...
$subdirs | ForEach-Object {
    Remove-Item "$tempdir\$_" -Recurse -Confirm
    Write-Output "removed '$tempdir\$_'"
}
