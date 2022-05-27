import logging
import pathlib

from notsotuf.repo import (
    DEFAULT_KEY_MAP, DEFAULT_KEYS_DIR_NAME, DEFAULT_REPO_DIR_NAME, Repository
)

from myapp.settings import APP_NAME

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
DEV_DIR = MODULE_DIR / 'temp'

# Local repo path and keys path (would normally be offline)
KEYS_DIR = DEV_DIR / DEFAULT_KEYS_DIR_NAME
REPO_DIR = DEV_DIR / DEFAULT_REPO_DIR_NAME

# Key settings
KEY_NAME = 'my_key'
PRIVATE_KEY_PATH = KEYS_DIR / KEY_NAME
KEY_MAP = {role_name: KEY_NAME for role_name in DEFAULT_KEY_MAP.keys()}
ENCRYPTED_KEYS = []

# Expiration dates
EXPIRATION_DAYS = dict(root=365, targets=7, snapshot=7, timestamp=1)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Create repository instance
    repo = Repository(
        app_name=APP_NAME,
        app_version_attr='myapp.settings.APP_VERSION',
        repo_dir=REPO_DIR,
        keys_dir=KEYS_DIR,
        key_map=KEY_MAP,
        expiration_days=EXPIRATION_DAYS,
        encrypted_keys=ENCRYPTED_KEYS,
    )

    # Save configuration (JSON file)
    repo.save_config()

    # Initialize repository (creates keys and root metadata, if necessary)
    repo.initialize()
