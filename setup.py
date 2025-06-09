import sys
import setup_env  # This must be imported first to set up the Python path
from cx_Freeze import setup, Executable
from myapp.settings import APP_VERSION

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["tufup"],
    "excludes": [],
    "include_files": [],
}

# MSI specific options
bdist_msi_options = {
    "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\tufup-example",
}

# GUI applications require a different base on Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="tufup-example",
    version=APP_VERSION,
    description="TUF Update Example Application",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options
    },
    executables=[
        Executable(
            "repo_init.py",
            base=base,
            target_name="tufup-example.exe" if sys.platform == "win32" else "tufup-example",
            icon=None,  # Add icon path here if you have one
        )
    ],
) 