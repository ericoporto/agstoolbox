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
    text_file_starts_with_xml_Windows1252, list_game_projects_in_dir

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
