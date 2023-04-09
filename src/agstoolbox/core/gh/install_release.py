import os
import zipfile

from agstoolbox.core.gh.download_release import get_zip_archive_cache_path
from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings.settings import Settings
from agstoolbox.core.utils.file import remove_dir_contents, mkdirp


def get_release_install_dir(release: Release) -> str:
    base_install_dir = Settings().get_editor_install_dir()
    return os.path.join(base_install_dir, release.version.as_str)


def is_install_dir_busy(release: Release) -> bool:
    install_dir = get_release_install_dir(release)
    dir_doesnt_exist: bool = not os.path.exists(install_dir)
    if dir_doesnt_exist:
        return False
    dir_exists_but_empty: bool = os.path.isdir(install_dir) and not os.listdir(install_dir)
    return not dir_exists_but_empty


def install_release_from_cache(release: Release):
    filepath_in_cache = get_zip_archive_cache_path(release)
    install_dir = get_release_install_dir(release)
    remove_dir_contents(install_dir)
    mkdirp(install_dir)
    with zipfile.ZipFile(filepath_in_cache, 'r') as zip_ref:
        zip_ref.extractall(install_dir)
