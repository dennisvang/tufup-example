import logging
import sys
import glob
import pathlib
import shutil
import tempfile

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
        print(f'Found MSI installer: {msi_file}')

        # Create a temporary copy of the MSI file
        temp_dir = pathlib.Path(tempfile.mkdtemp())
        temp_msi = temp_dir / msi_file.name
        print(f'Creating temporary copy in: {temp_dir}')
        shutil.copy2(msi_file, temp_msi)

        # Create repository instance from config file (assuming the repository
        # has already been initialized)
        repo = Repository.from_config()

        # Add new app bundle to repository (automatically reads myapp.__version__)
        print(f'Adding bundle to repository: {temp_msi}')
        repo.add_bundle(
            new_bundle_dir=temp_msi,
            # Skip patch creation to avoid deleting the original MSI file
            skip_patch=True,
            # [optional] custom metadata can be any dict (default is None)
            custom_metadata={'changes': ['new feature x added', 'bug y fixed']},
        )
        repo.publish_changes(private_key_dirs=[KEYS_DIR])

        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print('Done.')
    except FileNotFoundError:
        sys.exit(f'Directory not found: dist\nDid you run build_win.bat?')
    except Exception as e:
        print(f"Error: {e}")
        raise
