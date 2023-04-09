from __future__ import annotations  # for python 3.8

from agstoolbox.core.cmdline.progress import ProgressBar
from agstoolbox.core.gh.download_release import download_release_to_cache
from agstoolbox.core.gh.release import Release


def cmdline_download_release_to_cache(release: Release, quiet: bool):
    max_size: int = release.archive_size

    bar = None
    if not quiet:
        bar = ProgressBar(' Downloading... ', ' ' + release.archive_name + ' ', max_size, 'B')

    def progress_updates(completed_percent: float,
                         c_size: int,
                         acc_c_size: int,
                         total_size_in_bytes: int):
        if bar is not None:
            bar.update(int(acc_c_size/8), total_size_in_bytes)

    download_release_to_cache(release, progress_updates)

    if bar is not None:
        bar.finish()
