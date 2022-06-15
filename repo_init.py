import logging

from notsotuf.repo import Repository

from myapp.settings import APP_NAME
from repo_settings import (
    ENCRYPTED_KEYS, EXPIRATION_DAYS, KEY_MAP, KEYS_DIR, REPO_DIR, THRESHOLDS
)

logger = logging.getLogger(__name__)

"""

DISCLAIMER 

For convenience, this example uses a single key pair for all TUF roles, 
and the private key is unencrypted and stored locally. This approach is *not* 
safe and should *not* be used in production. 

"""

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
        thresholds=THRESHOLDS,
    )

    # Save configuration (JSON file)
    repo.save_config()

    # Initialize repository (creates keys and root metadata, if necessary)
    repo.initialize()
