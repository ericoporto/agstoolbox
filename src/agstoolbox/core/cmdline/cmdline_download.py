from __future__ import annotations  # for python 3.8

from agstoolbox.core.cmdline.progress import ProgressBar
from agstoolbox.core.gh.download_release import download_release_to_cache
from agstoolbox.core.gh.release import Release


def cmdline_download_release_to_cache(release: Release):
    bar = ProgressBar(' downloading... ', ' ' + release.archive_name + ' ', release.archive_size)

    def progress_updates(completed_percent: float,
                         c_size: int,
                         acc_c_size: int,
                         total_size_in_bytes: int):
        bar.update(int(acc_c_size/8), total_size_in_bytes)

    download_release_to_cache(release, progress_updates)

    bar.finish()
