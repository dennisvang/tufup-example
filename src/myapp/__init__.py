import logging
import shutil

from notsotuf.client import Client

from myapp import settings

logger = logging.getLogger(__name__)


def update(pre: str):
    # Create update client
    client = Client(
        app_name=settings.APP_NAME,
        app_install_dir=settings.INSTALL_DIR,
        current_version=settings.CURRENT_VERSION,
        metadata_dir=settings.METADATA_DIR,
        metadata_base_url=settings.METADATA_BASE_URL,
        target_dir=settings.TARGET_DIR,
        target_base_url=settings.TARGET_BASE_URL,
        refresh_required=False,
    )

    # Perform update
    client.update(pre=pre)


def main(cmd_args):
    # extract options from command line args
    pre_release_channel = cmd_args[0] if cmd_args else None  # 'a', 'b', or 'rc'

    # The app must ensure dirs exist
    for dir_path in [settings.INSTALL_DIR, settings.METADATA_DIR, settings.TARGET_DIR]:
        dir_path.mkdir(exist_ok=True, parents=True)

    # The app must be shipped with a trusted "root.json" metadata file,
    # which is created using the notsotuf.repo tools. The app must ensure
    # this file can be found in the specified metadata_dir. The root metadata
    # file lists all trusted keys and TUF roles.
    source_path = settings.MODULE_DIR.parent / 'root.json'
    destination_path = settings.METADATA_DIR / 'root.json'
    if not destination_path.exists():
        shutil.copy(src=source_path, dst=destination_path)
        logger.info('Trusted root metadata copied to cache.')

    # Download and apply any available updates
    update(pre=pre_release_channel)

    # Do what the app is supposed to do
    print(f'Starting {settings.APP_NAME} {settings.CURRENT_VERSION}...')
    ...
    print('Doing what the app is supposed to do...')
    ...
    print('Done.')
