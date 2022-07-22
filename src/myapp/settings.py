import logging
import os
import pathlib
import sys

logger = logging.getLogger(__name__)

# App info
APP_NAME = 'my_app'
APP_VERSION = '2.0'

# On Windows 10, a typical location for app data would be %PROGRAMDATA%\MyApp
# (per-machine), or %LOCALAPPDATA%\MyApp (per-user). Typical app installation
# locations are %PROGRAMFILES%\MyApp (per-machine) or
# %LOCALAPPDATA%\Programs\MyApp (per-user). Also see:
# https://docs.microsoft.com/en-us/windows/win32/msi/installation-context

# Windows per-machine paths
WIN_PER_MACHINE_PROGRAMS_DIR = pathlib.Path(os.getenv('ProgramFiles'))
WIN_PER_MACHINE_DATA_DIR = pathlib.Path(os.getenv('PROGRAMDATA'))

# Windows per-user paths
WIN_PER_USER_DATA_DIR = pathlib.Path(os.getenv('LOCALAPPDATA'))
WIN_PER_USER_PROGRAMS_DIR = WIN_PER_USER_DATA_DIR / 'Programs'

# Current module dir (when frozen this equals sys._MEIPASS)
# https://pyinstaller.org/en/stable/runtime-information.html#using-file
MODULE_DIR = pathlib.Path(__file__).resolve().parent

# Are we running in a PyInstaller bundle?
# https://pyinstaller.org/en/stable/runtime-information.html
FROZEN = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')

# For development
DEV_DIR = MODULE_DIR.parent.parent / 'temp'

# App directories
PROGRAMS_DIR = WIN_PER_USER_PROGRAMS_DIR if FROZEN else DEV_DIR
DATA_DIR = WIN_PER_USER_DATA_DIR if FROZEN else DEV_DIR
INSTALL_DIR = PROGRAMS_DIR / APP_NAME
UPDATE_CACHE_DIR = DATA_DIR / APP_NAME / 'update_cache'
METADATA_DIR = UPDATE_CACHE_DIR / 'metadata'
TARGET_DIR = UPDATE_CACHE_DIR / 'targets'

# Update-server urls
METADATA_BASE_URL = 'http://localhost:8000/metadata/'
TARGET_BASE_URL = 'http://localhost:8000/targets/'

# Location of trusted root metadata file
TRUSTED_ROOT_SRC = MODULE_DIR.parent / 'root.json'
if not FROZEN:
    # for development, get the root metadata directly from local repo
    TRUSTED_ROOT_SRC = MODULE_DIR.parent.parent / 'repo/deploy/metadata/root.json'
TRUSTED_ROOT_DST = METADATA_DIR / 'root.json'
