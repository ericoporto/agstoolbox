from __future__ import annotations  # for python 3.8
import os.path
from typing import Callable

from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings.settings import ConstSettings
from agstoolbox.core.utils.downloader import download_from_url
from agstoolbox.core.utils.file import remove_dir_contents, mkdirp


def get_cache_dir(release: Release) -> str:
    return os.path.join(ConstSettings().cache_dir, "editor", release.version.as_str)


def get_zip_archive_cache_path(release: Release):
    cache_dir = get_cache_dir(release)
    return os.path.join(cache_dir, release.archive_name)


def download_release_to_cache(release: Release,
                              progress_update: Callable[[float, int, int, int], None] = None):
    r_url = release.archive_url
    filepath_in_cache = get_zip_archive_cache_path(release)
    remove_dir_contents(filepath_in_cache)
    cache_dir = get_cache_dir(release)
    mkdirp(cache_dir)
    download_from_url(url=r_url,
                      save_path=filepath_in_cache,
                      progress_update=progress_update)
