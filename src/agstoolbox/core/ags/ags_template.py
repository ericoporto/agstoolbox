from __future__ import annotations  # for python 3.8

import fnmatch
import os
import re
from shutil import move as shutil_move
from typing import List
from pathlib import Path

from agstoolbox.core.ags.ags_editor_versions import is_ags4
from agstoolbox.core.ags.datafile_writer import get_multifile_lib, make_data_file_from_multifile_lib
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.multifilelib import MultiFileLib
from agstoolbox.core.utils.file import join_paths_as_posix, get_file_if_exists, get_absolute_path, \
    get_posix
from agstoolbox.core.version.version import Version
from agstoolbox.core.version.version_utils import version_str_to_version, \
    is_version_a_bigger_than_b, is_version_a_between_bc


def case_insensitive_glob(directory: str, file_mask: str) -> list[Path]:
    reg_expr = re.compile(fnmatch.translate(file_mask), re.IGNORECASE)
    list_path = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory, i))]
    result = [os.path.join(directory, j) for j in list_path if re.match(reg_expr, j)]
    result = [Path(j) for j in result]
    if result is None:
        return []
    return result


def get_dir_file_list(directory: str, file_mask: str):
    try:
        path = Path(directory).as_posix()
        return case_insensitive_glob(path, file_mask)
    except IOError:
        return []


def add_matching_files(file_list: List[str], file_mask: str, parent_dir: str,
                       full_paths: bool = False):
    files = get_dir_file_list(parent_dir, file_mask)
    if full_paths:
        file_list.extend([str(file) for file in files])
    else:
        file_list.extend([str(file.relative_to(parent_dir)) for file in files])


def construct_template_filelist(parent_dir: str) -> List[str]:
    files_to_include: List[str] = list()
    add_matching_files(files_to_include, "*.ico", parent_dir)
    add_matching_files(files_to_include, "Game.agf", parent_dir)
    add_matching_files(files_to_include, "acsprset.spr", parent_dir)
    add_matching_files(files_to_include, "preload.pcx", parent_dir)
    add_matching_files(files_to_include, "AudioCache/*.*", parent_dir)
    add_matching_files(files_to_include, "Speech/*.*", parent_dir)
    add_matching_files(files_to_include, "flic*.fl?", parent_dir)
    add_matching_files(files_to_include, "agsfnt*.ttf", parent_dir)
    add_matching_files(files_to_include, "agsfnt*.wfn", parent_dir)
    add_matching_files(files_to_include, "*.crm", parent_dir)
    add_matching_files(files_to_include, "*.asc", parent_dir)
    add_matching_files(files_to_include, "*.ash", parent_dir)
    add_matching_files(files_to_include, "*.txt", parent_dir)
    add_matching_files(files_to_include, "*.trs", parent_dir)
    add_matching_files(files_to_include, "*.pdf", parent_dir)
    add_matching_files(files_to_include, "*.ogv", parent_dir)
    return files_to_include


def create_template_from_game_dir(project_dir: str, template_filepath: str):
    if Path(template_filepath).exists():
        Path(template_filepath).unlink()

    template_filename: str = Path(template_filepath).name
    template_dir: str = str(Path(template_filepath).parent.as_posix())

    template_filelist: List[str] = construct_template_filelist(project_dir)
    filelist: List[str] = list()
    for file in template_filelist:
        filelist.append(join_paths_as_posix(project_dir, file))

    mlib: MultiFileLib = get_multifile_lib(filelist, project_dir, template_filename, False)
    make_data_file_from_multifile_lib(mlib, template_dir)


# the command below builds using a reimplemented template export
# the one using the editor is in ags_local_run
def create_template_from_project(game_project: GameProject, template_name: str, out: str | None):
    if out is None:
        out = game_project.directory

    template_name = Path(template_name).name
    template_filepath: str = join_paths_as_posix(out, template_name)
    create_template_from_game_dir(game_project.directory, template_filepath)


# Note, in ags
# v4.0.0.9, v4.0.0.10 ...
# and
# v3.6.2.1, v3.6.2.2 ...
# /template command is supported in the Editor
def editor_supports_template_export(game_project: GameProject) -> bool:
    ags3_first_sup: Version = version_str_to_version('3.6.2.1')
    ags4_first_sup: Version = version_str_to_version('4.0.0.9')
    ags3_to_ags4_ver: Version = version_str_to_version('3.99.0.0')
    ags4: bool = is_ags4(game_project.ags_editor_version)
    if ags4:
        return is_version_a_bigger_than_b(game_project.ags_editor_version, ags4_first_sup)
    else:
        return is_version_a_between_bc(game_project.ags_editor_version, ags3_first_sup, ags3_to_ags4_ver)


# Template built with editor uses instead GameFileName + ".agt"
def fix_editor_built_template(game_project: GameProject, out_dir: str, filename: str) -> bool:
    built_dir: str = game_project.directory
    built_file: str = game_project.game_file + ".agt"
    built_filename = get_file_if_exists(built_dir, built_file)
    if built_filename is None:
        return False

    built_filename = get_posix(get_absolute_path(built_filename))
    target_filename: str = get_posix(get_absolute_path(os.path.join(out_dir, filename)))
    if target_filename == built_filename:
        # no need to do anything
        return True

    existing_target_filename: str = get_file_if_exists(out_dir, filename)
    if existing_target_filename is not None:
        shutil_move(existing_target_filename, existing_target_filename + ".bkp")

    shutil_move(built_filename, target_filename)
    return True
