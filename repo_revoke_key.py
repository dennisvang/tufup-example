import logging
from tufup.repo import Keys, Roles, TOP_LEVEL_ROLE_NAMES, in_

from repo_init import KEY_NAME, KEYS_DIR, METADATA_DIR

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # load metadata
    keys = Keys(dir_path=KEYS_DIR, encrypted=[])
    for role_name in TOP_LEVEL_ROLE_NAMES:
        keys.import_public_key(role_name=role_name, key_name=KEY_NAME)
    roles = Roles(dir_path=METADATA_DIR, encrypted=[])

    # create new key pair
    new_private_key_path = KEYS_DIR / 'new_key'
    new_public_key_path = Keys.create_key_pair(
        private_key_path=new_private_key_path, encrypted=False
    )

    # replace the first root key (automatically saves the new root file)
    roles.replace_key(
        old_key_id=next(iter(roles.root.signed.keys.keys())),
        old_private_key_path=KEYS_DIR / 'my_key',
        new_private_key_path=new_private_key_path,
        new_public_key_path=new_public_key_path,
        root_expires=in_(365),
    )
