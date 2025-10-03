import logging
import pathlib
import subprocess
from tempfile import TemporaryDirectory

from tufup.common import DefaultBinaryDiff
from tufup.utils.platform_specific import ON_MAC, ON_WINDOWS

"""
[OPTIONAL]

This is an example of a custom binary diff/patch implementation.

This example uses [HDiffPatch], based on the [comment from mchaniotakis].

[HDiffPatch]: https://github.com/sisong/HDiffPatch/releases
[comment from mchaniotakis]: https://github.com/dennisvang/tufup/issues/154#issuecomment-2227945468
"""

logger = logging.getLogger(__name__)

LIBRARY_NAME = 'hdiffpatch_v4.12.0'
MODULE_DIR = pathlib.Path(__file__).resolve().parent


def _executable_path(action: str) -> str:
    """
    Determine executable path for current platform. This could be done with a simple
    string instead, if we weren't handling multiple platforms.

    action: 'diff' or 'patch'
    """
    os_name = 'linux64'
    suffix = ''
    if ON_MAC:
        os_name = 'macos'
    elif ON_WINDOWS:
        os_name = 'windows64'
        suffix = '.exe'
    executable_path = MODULE_DIR / LIBRARY_NAME / os_name / f'h{action}z{suffix}'
    logger.info(f'using {LIBRARY_NAME}: {executable_path}')
    return str(executable_path)


class HDiffPatch(DefaultBinaryDiff):
    """
    In this case we're only interested in using a custom diff, using HDiffPatch to
    produce a bsdiff4-compatible diff. So, we only override the diff method.
    """

    @staticmethod
    def diff(*, src_bytes: bytes, dst_bytes: bytes) -> bytes:
        patch_bytes = b''
        with TemporaryDirectory() as temp_dir:
            # ugly workaround because HDiffPatch only accepts files
            # (names matching HDiffPatch args)
            temp_dir_path = pathlib.Path(temp_dir)
            old_path = temp_dir_path / 'old'
            old_path.write_bytes(src_bytes)
            new_path = temp_dir_path / 'new'
            new_path.write_bytes(dst_bytes)
            out_diff_file = temp_dir_path / 'diff'
            logger.info(f'creating diff: {out_diff_file}')
            # https://github.com/sisong/HDiffPatch?tab=readme-ov-file#diff-command-line-usage
            completed_process = subprocess.run(
                [
                    _executable_path('diff'),  # executable path
                    '-s-4k',  # load as stream, blocksize 4k
                    '-BSD',  # compatible with bsdiff4
                    str(old_path),
                    str(new_path),
                    str(out_diff_file),
                ],
                capture_output=True,
            )
            # raise CalledProcessError if process failed
            completed_process.check_returncode()
            # read bytes from temporary file
            patch_bytes = out_diff_file.read_bytes()
        return patch_bytes
