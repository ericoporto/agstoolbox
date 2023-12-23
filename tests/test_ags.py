#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path


# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.utils.file import join_paths_as_posix
from agstoolbox.core.ags.get_game_projects import is_game_file, \
    text_file_starts_with_xml_Windows1252, list_game_projects_in_dir, \
    get_unique_game_project_in_path
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.get_script_module import module_from_game_project, \
    exists_module_in_game_project

cur_dir = Path(__file__).resolve().parent
file_path01 = join_paths_as_posix(cur_dir, 'resources/fakedir2/Game.agf')
file_path02 = join_paths_as_posix(cur_dir, 'resources/fakedir2/fakedirA/Game.agf')
file_path03 = join_paths_as_posix(cur_dir, 'resources/fakedir3/fakedir3/CopyGame/Game.agf')
file_path04 = join_paths_as_posix(cur_dir, 'resources/otherfakedir/MinGame/Game.agf')


def test_text_file_starts_with_xml_Windows1252():
    assert text_file_starts_with_xml_Windows1252(file_path01) is False
    assert text_file_starts_with_xml_Windows1252(file_path02) is False
    assert text_file_starts_with_xml_Windows1252(file_path03) is True
    assert text_file_starts_with_xml_Windows1252(file_path04) is True


def test_is_game_file():
    assert is_game_file(file_path01) is False
    assert is_game_file(file_path02) is False
    assert is_game_file(file_path03) is True
    assert is_game_file(file_path04) is True


def test_list_game_projects_in_dir():
    projects = list_game_projects_in_dir(cur_dir.as_posix())
    assert len(projects) == 2
    proj_copy_game = next((p for p in projects if p.name == 'CopyGameTitle'), None)
    proj_min_game = next((p for p in projects if p.name == 'MinGame'), None)
    assert proj_copy_game is not None
    assert proj_min_game is not None


def test_get_unique_game_project_in_path():
    assert get_unique_game_project_in_path(file_path01) is None
    assert get_unique_game_project_in_path(file_path02) is None
    assert get_unique_game_project_in_path(file_path03) is not None
    assert get_unique_game_project_in_path(file_path04) is not None
    game_project: GameProject = get_unique_game_project_in_path(file_path03)
    assert game_project.name == "CopyGameTitle"
    assert game_project.ags_editor_version.as_str == "3.5.1.14"


def test_script_module_from_game_file():
    game_proj03 = get_unique_game_project_in_path(file_path03)
    game_proj04 = get_unique_game_project_in_path(file_path04)

    assert exists_module_in_game_project(game_proj03, "GlobalScript") is True
    assert exists_module_in_game_project(game_proj04, "GlobalScript") is True

    sm03 = module_from_game_project(game_proj03, "GlobalScript")
    assert sm03 is not None
    assert sm03.unique_key == "764688079"
    assert sm03.unique_key_int == 764688079
    assert sm03.header.startswith("// Main header script") is True
    assert sm03.script.startswith("// main global script file") is True
    sm04 = module_from_game_project(game_proj04, "GlobalScript")
    assert sm04 is not None
    assert sm04.unique_key == "764688079"
    assert sm04.unique_key_int == 764688079
    assert sm04.header.startswith("// Main header script") is True
    assert sm04.script.startswith("// main global script file") is True
