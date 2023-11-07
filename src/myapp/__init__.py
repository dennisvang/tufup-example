import logging
import shutil
import time

from tufup.client import Client

from myapp import settings

logger = logging.getLogger(__name__)

__version__ = settings.APP_VERSION


def progress_hook(bytes_downloaded: int, bytes_expected: int):
    progress_percent = bytes_downloaded / bytes_expected * 100
    print(f'\r{progress_percent:.1f}%', end='')
    time.sleep(0.2)  # quick and dirty: simulate slow or large download
    if progress_percent >= 100:
        print('')


def update(pre: str, skip_confirmation: bool = False):
    # Create update client
    client = Client(
        app_name=settings.APP_NAME,
        app_install_dir=settings.INSTALL_DIR,
        current_version=settings.APP_VERSION,
        metadata_dir=settings.METADATA_DIR,
        metadata_base_url=settings.METADATA_BASE_URL,
        target_dir=settings.TARGET_DIR,
        target_base_url=settings.TARGET_BASE_URL,
        refresh_required=False,
    )

    # Perform update
    new_update = client.check_for_updates(pre=pre)
    if new_update:
        # At this point, the version info from `new_update` could be used to
        # present a custom confirmation dialog, asking the user if they wish
        # to proceed with the download (and installation). However, to keep
        # the example minimal, we simply rely on the built-in command-line
        # confirmation in download_and_apply_update().
        client.download_and_apply_update(
            skip_confirmation=skip_confirmation,
            progress_hook=progress_hook,
            # WARNING: Be very careful with `purge_dst_dir=True`, because
            # this will *irreversibly* delete *EVERYTHING* inside the
            # `app_install_dir`, except any paths specified in
            # `exclude_from_purge`. So, *ONLY* use `purge_dst_dir=True` if
            # you are absolutely certain that your `app_install_dir` does not
            # contain any unrelated content.
            purge_dst_dir=False,
            exclude_from_purge=None,
            log_file_name='install.log',
        )


def main(cmd_args):
    # a proper app would use argparse, but we just do minimal argument
    # parsing to keep things simple
    pre_release_channel = None
    skip_confirmation = False
    while cmd_args:
        arg = cmd_args.pop(0)
        if arg in ['a', 'b', 'rc']:
            pre_release_channel = arg
        else:
            skip_confirmation = arg == 'skip'

    # The app must ensure dirs exist
    for dir_path in [settings.INSTALL_DIR, settings.METADATA_DIR, settings.TARGET_DIR]:
        dir_path.mkdir(exist_ok=True, parents=True)

    # The app must be shipped with a trusted "root.json" metadata file,
    # which is created using the tufup.repo tools. The app must ensure
    # this file can be found in the specified metadata_dir. The root metadata
    # file lists all trusted keys and TUF roles.
    if not settings.TRUSTED_ROOT_DST.exists():
        shutil.copy(src=settings.TRUSTED_ROOT_SRC, dst=settings.TRUSTED_ROOT_DST)
        logger.info('Trusted root metadata copied to cache.')

    # Download and apply any available updates
    update(pre=pre_release_channel, skip_confirmation=skip_confirmation)

    # Do what the app is supposed to do
    print(f'Starting {settings.APP_NAME} {settings.APP_VERSION}...')
    ...
    print('Doing what the app is supposed to do...')
    ...
    print('Done.')
