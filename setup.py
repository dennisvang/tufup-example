import sys
import os
from cx_Freeze import setup, Executable

# Get APP_DIR from command line args or use default
APP_DIR = "temp_my_app"
if len(sys.argv) > 1 and sys.argv[1] == "bdist_msi":
    for i, arg in enumerate(sys.argv):
        if arg == "--app-dir" and i + 1 < len(sys.argv):
            APP_DIR = sys.argv[i + 1]
            sys.argv.pop(i)  # Remove --app-dir
            sys.argv.pop(i)  # Remove the value
            break

# Constants for directories
DIST_DIR = os.path.join(APP_DIR, "dist")
DIST_DIR_MAIN = os.path.join(DIST_DIR, "main")

# Version from myapp.settings
from myapp.settings import APP_VERSION as version
print(f"\nUsing version from myapp.settings: {version}")  # Debug print

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["tufup", "tufup.client", "tufup.repo", "tufup.utils"],
    "includes": ["tufup"],
    "excludes": [],
    "include_files": [],
}

# MSI specific options
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
    "add_to_path": True,  # Add to PATH so it can be run from anywhere
    "initial_target_dir": r"[LocalAppDataFolder]\tufup-example",  # Install in user's AppData folder
    "dist_dir": DIST_DIR_MAIN if version == "1.0" else DIST_DIR,  # Use main subdir for v1.0
    "target_name": "tufup-example",  # Base name without version - MSI builder will add version
}

print(f"\nMSI build options:")
print(f"  - Version: {version}")
print(f"  - Dist dir: {bdist_msi_options['dist_dir']}")
print(f"  - Install dir: {bdist_msi_options['initial_target_dir']}")
print(f"  - Target name: {bdist_msi_options['target_name']}")

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Only include cx_Freeze specific options when not installing
if len(sys.argv) > 1 and sys.argv[1] not in ['install', 'develop', 'editable_wheel']:
    options = {
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    }
else:
    options = {}

# Always include at least one executable
executables = [
    Executable(
        "repo_init.py",
        base=base,
        target_name="tufup-example.exe" if sys.platform == "win32" else "tufup-example",
        icon=None,  # Add icon path here if you have one
    )
]

setup(
    name="tufup-example",
    version=version,  # This will be used for the MSI version
    description="TUF Update Example Application",
    options=options,
    executables=executables,
) 