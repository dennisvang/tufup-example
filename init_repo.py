import logging
import pathlib

from notsotuf.repo import Keys, Roles, TOP_LEVEL_ROLE_NAMES, in_

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
REPO_DIR = DEV_DIR / 'repo'
KEYS_DIR = REPO_DIR / 'keystore'
DEPLOY_DIR = REPO_DIR / 'deploy'
METADATA_DIR = DEPLOY_DIR / 'metadata'
TARGETS_DIR = DEPLOY_DIR / 'targets'

# Key settings
KEY_NAME = 'my_key'
KEY_MAP = {role_name: KEY_NAME for role_name in TOP_LEVEL_ROLE_NAMES}
PRIVATE_KEY_PATH = KEYS_DIR / KEY_NAME
ENCRYPTED_KEYS = []

# Expiration dates
ROOT_EXPIRATION_DATE = in_(365)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Ensure dirs exist
    for path in [KEYS_DIR, METADATA_DIR, TARGETS_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    # For convenience, we use a single, unencrypted, key pair for all tuf
    # roles. This is *not* recommended for production.
    keys = Keys(dir_path=KEYS_DIR, encrypted=ENCRYPTED_KEYS, key_map=KEY_MAP)
    keys.create()  # safe to call if keys already exist

    # Initialize root metadata object
    roles = Roles(dir_path=METADATA_DIR)

    if not roles.root:
        # Register keys
        roles.initialize(keys=keys)

        # Publish metadata (saves root.json file)
        roles.publish_root(
            private_key_paths=[PRIVATE_KEY_PATH], expires=ROOT_EXPIRATION_DATE
        )
