import logging
import sys

from notsotuf.repo import Repository

from init_repo import DEV_DIR
from myapp.settings import CURRENT_VERSION

logger = logging.getLogger(__name__)

PYINSTALLER_DIST_DIR_NAME = 'dist'
DIST_DIR = DEV_DIR / PYINSTALLER_DIST_DIR_NAME

if __name__ == '__main__':
    # create archive from latest pyinstaller bundle (assuming we have already
    # created a pyinstaller bundle, and there is only one)
    try:
        bundle_dirs = [path for path in DIST_DIR.iterdir() if path.is_dir()]
    except FileNotFoundError:
        sys.exit(f'Directory not found: {DIST_DIR}\nDid you run pyinstaller?')
    if len(bundle_dirs) != 1:
        sys.exit(f'Expected one bundle, found {len(bundle_dirs)}.')
    bundle_dir = bundle_dirs[0]

    # Create repository instance from config file (assuming the repository
    # has already been initialized)
    repo = Repository.from_config()

    # Add new app bundle to repository
    repo.add_bundle(new_version=CURRENT_VERSION, new_bundle_dir=bundle_dir)
