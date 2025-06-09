import logging
import sys
import glob
import pathlib

from tufup.repo import Repository

from repo_settings import DIST_DIR, KEYS_DIR

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    # create archive from latest MSI installer (assuming we have already
    # created a bundle, and there is only one)
    try:
        # cx_Freeze creates an MSI file in the dist directory
        msi_files = list(pathlib.Path('dist').glob('*.msi'))
        if not msi_files:
            sys.exit(f'No MSI installer found in dist directory\nDid you run build_win.bat?')
        if len(msi_files) != 1:
            sys.exit(f'Expected one MSI file, found {len(msi_files)}.')
        msi_file = msi_files[0]
        print(f'Adding MSI installer: {msi_file}')

        # Create repository instance from config file (assuming the repository
        # has already been initialized)
        repo = Repository.from_config()

        # Add new app bundle to repository (automatically reads myapp.__version__)
        repo.add_bundle(
            new_bundle_dir=msi_file,
            # [optional] custom metadata can be any dict (default is None)
            custom_metadata={'changes': ['new feature x added', 'bug y fixed']},
        )
        repo.publish_changes(private_key_dirs=[KEYS_DIR])

        print('Done.')
    except FileNotFoundError:
        sys.exit(f'Directory not found: dist\nDid you run build_win.bat?')
