import os.path

from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings import ConstSettings
from agstoolbox.core.utils.downloader import download_from_url
from agstoolbox.core.utils.file import remove_dir_contents


def get_zip_archive_cache_path(release: Release):
    cache_dir = os.path.join(ConstSettings().cache_dir, "editor", release.version)
    return os.path.join(cache_dir, release.archive_name)


def download_release_to_cache(release: Release):
    r_url = release.archive_url
    filepath_in_cache = get_zip_archive_cache_path(release)
    remove_dir_contents(filepath_in_cache)
    download_from_url(url=r_url, save_path=filepath_in_cache)
