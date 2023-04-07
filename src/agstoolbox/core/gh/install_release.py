import os
import zipfile

from agstoolbox.core.gh.download_release import get_zip_archive_cache_path
from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings.settings import Settings
from agstoolbox.core.utils.file import remove_dir_contents, mkdirp


def install_release_from_cache(release: Release):
    filepath_in_cache = get_zip_archive_cache_path(release)
    base_install_dir = Settings().get_editor_install_dir()
    install_dir = os.path.join(base_install_dir, release.version.as_str)
    remove_dir_contents(install_dir)
    mkdirp(install_dir)
    with zipfile.ZipFile(filepath_in_cache, 'r') as zip_ref:
        zip_ref.extractall(install_dir)
