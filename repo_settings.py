import logging
import pathlib

from tufup.repo import DEFAULT_KEY_MAP, DEFAULT_KEYS_DIR_NAME, DEFAULT_REPO_DIR_NAME

logger = logging.getLogger(__name__)

"""

DISCLAIMER 

For convenience, this example uses a single key pair for all TUF roles, 
and the private key is unencrypted and stored locally. This approach is *not* 
safe and should *not* be used in production. 

"""

# Path to directory containing current module
MODULE_DIR = pathlib.Path(__file__).resolve().parent

# For development
DEV_DIR = MODULE_DIR / 'temp_my_app'
BUILD_DIR = MODULE_DIR / 'build'
DIST_DIR = BUILD_DIR  # cx_Freeze uses the build directory

# Local repo path and keys path (would normally be offline)
KEYS_DIR = DEV_DIR / DEFAULT_KEYS_DIR_NAME
REPO_DIR = DEV_DIR / DEFAULT_REPO_DIR_NAME

# Key settings
KEY_NAME = 'my_key'
PRIVATE_KEY_PATH = KEYS_DIR / KEY_NAME
KEY_MAP = {role_name: [KEY_NAME] for role_name in DEFAULT_KEY_MAP.keys()}
ENCRYPTED_KEYS = []
THRESHOLDS = dict(root=1, targets=1, snapshot=1, timestamp=1)
EXPIRATION_DAYS = dict(root=365, targets=7, snapshot=7, timestamp=1)
