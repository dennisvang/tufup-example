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

# Local repo path and keys path (would normally be offline)
REPO_DIR = MODULE_DIR / 'repo'
KEYS_DIR = REPO_DIR / 'keystore'
DEPLOY_DIR = REPO_DIR / 'deploy'
METADATA_DIR = DEPLOY_DIR / 'metadata'
TARGETS_DIR = DEPLOY_DIR / 'targets'

# Private key path
KEY_NAME = 'my_key'
PRIVATE_KEY_PATH = KEYS_DIR / KEY_NAME

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Ensure dirs exist
    for path in [KEYS_DIR, METADATA_DIR, TARGETS_DIR]:
        path.mkdir(parents=True, exist_ok=True)

    # For convenience, we use a single key pair for all tuf roles. This is *not*
    # recommended.
    if not PRIVATE_KEY_PATH.exists():
        public_key_path = Keys.create_key_pair(
            private_key_path=PRIVATE_KEY_PATH, encrypted=False
        )

    # Import the same public key for all roles
    keys = Keys(dir_path=KEYS_DIR, encrypted=[])
    for role_name in TOP_LEVEL_ROLE_NAMES:
        keys.import_public_key(role_name=role_name, key_name=KEY_NAME)

    # Initialize root metadata object
    roles = Roles(dir_path=METADATA_DIR, encrypted=[])

    if not roles.root:
        # Register keys
        roles.initialize(keys=keys)

        # Publish metadata (saves root.json file)
        roles.publish_root(private_key_paths=[PRIVATE_KEY_PATH], expires=in_(365))
