from __future__ import annotations  # for python 3.8

from pathlib import Path

from agstoolbox.core.ags.game_project import (GameProject,
                                              COMPILED_WEB_DIR_NAME,
                                              COMPILED_LINUX_DIR_NAME,
                                              COMPILED_WINDOWS_DIR_NAME)
from agstoolbox.core.ags.game_project_compiled import from_project_get_compiled_dirs
from agstoolbox.core.utils.archive import zip_dir, tar_gz_dir
from agstoolbox.core.utils.file import join_paths_as_posix, mkdirp


def package_compiled_game(project: GameProject):
    compiled_dirs: list[str] = from_project_get_compiled_dirs(project)
    game_file = project.game_file
    dist_dir = join_paths_as_posix(project.directory, 'Dist')
    mkdirp(dist_dir)

    for d in compiled_dirs:
        if Path(d).name == COMPILED_WINDOWS_DIR_NAME:
            archive_name = game_file + '_windows.zip'
            out_file_path = join_paths_as_posix(dist_dir, archive_name)
            zip_dir(d, out_file_path)
        if Path(d).name == COMPILED_WEB_DIR_NAME:
            archive_name = game_file + '_web.zip'
            out_file_path = join_paths_as_posix(dist_dir, archive_name)
            zip_dir(d, out_file_path)
        if Path(d).name == COMPILED_LINUX_DIR_NAME:
            archive_name = game_file + '_linux.tar.gz'
            out_file_path = join_paths_as_posix(dist_dir, archive_name)
            tar_gz_dir(d, out_file_path, [game_file, 'data/ags32', 'data/ags64'])
