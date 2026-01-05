from __future__ import annotations  # for python 3.8

from pathlib import Path

from agstoolbox.core.utils.file import join_paths_as_posix, dir_is_valid
from agstoolbox.core.ags.game_project import (GameProject,
                                              COMPILED_WEB_DIR_NAME,
                                              COMPILED_LINUX_DIR_NAME,
                                              COMPILED_WINDOWS_DIR_NAME)

def from_project_get_compiled_dirs(project: GameProject) -> list[str]:
    project_dir = project.directory
    possible_subdirs = [COMPILED_WINDOWS_DIR_NAME, COMPILED_LINUX_DIR_NAME, COMPILED_WEB_DIR_NAME]

    candidate_compiled_dirs = []
    for d in possible_subdirs:
        cdir = join_paths_as_posix(join_paths_as_posix(project_dir, 'Compiled'), d)
        if dir_is_valid(cdir):
            candidate_compiled_dirs.append(cdir)

    compiled_dirs = []
    game_file = project.game_file
    for d in candidate_compiled_dirs:
        if Path(d).name == COMPILED_WINDOWS_DIR_NAME:
            files_exist: bool = True
            files_exist &= Path(join_paths_as_posix(d,game_file + '.exe')).exists()
            if files_exist:
                compiled_dirs.append(d)
        if Path(d).name == COMPILED_WEB_DIR_NAME:
            files_exist: bool = True
            files_exist &= Path(join_paths_as_posix(d,'index.html')).exists()
            files_exist &= Path(join_paths_as_posix(d,'ags.js')).exists()
            files_exist &= Path(join_paths_as_posix(d,'ags.wasm')).exists()
            files_exist &= Path(join_paths_as_posix(d,game_file + '.ags')).exists()
            if files_exist:
                compiled_dirs.append(d)
        if Path(d).name == COMPILED_LINUX_DIR_NAME:
            files_exist: bool = True
            data_dir = join_paths_as_posix(d,'data')
            files_exist &= Path(join_paths_as_posix(data_dir, game_file + '.ags')).exists()
            files_exist &= Path(join_paths_as_posix(data_dir,'ags64')).exists()
            if files_exist:
                compiled_dirs.append(d)

    return compiled_dirs
