import os
import zipfile
from pathlib import Path

from agstoolbox.core.gh.download_release import get_zip_archive_cache_path
from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings import ConstSettings, Settings
from agstoolbox.core.utils.file import remove_dir_contents


def install_release_from_cache(release: Release):
    filepath_in_cache = get_zip_archive_cache_path(release)
    base_install_dir = Settings().get_editor_install_dir()
    instal_dir = os.path.join(base_install_dir, release.version)
    Path(instal_dir).mkdir(parents=True, exist_ok=True)
    remove_dir_contents(instal_dir)
    with zipfile.ZipFile(filepath_in_cache, 'r') as zip_ref:
        zip_ref.extractall(instal_dir)