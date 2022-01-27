#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(
        os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.ags.get_game_projects import get_gp_candidates_in_dir, \
    is_game_file, text_file_starts_with_xml_Windows1252

cur_dir = Path(__file__).resolve().parent
file_path01 = Path(os.path.join(cur_dir, 'resources/fakedir2/Game.agf')).as_posix()
file_path02 = Path(os.path.join(cur_dir, 'resources/fakedir2/fakedirA/Game.agf')).as_posix()
file_path03 = Path(os.path.join(cur_dir, 'resources/fakedir3/fakedir3/CopyGame/Game.agf')).as_posix()
file_path04 = Path(os.path.join(cur_dir, 'resources/otherfakedir/MinGame/Game.agf')).as_posix()


def test_get_gp_candidates_in_dir():
    print(cur_dir.as_posix())
    candidates = get_gp_candidates_in_dir(cur_dir.as_posix())
    assert len(candidates) == 4
    c0 = Path(os.path.relpath(candidates[0], cur_dir)).as_posix()
    c1 = Path(os.path.relpath(candidates[1], cur_dir)).as_posix()
    c2 = Path(os.path.relpath(candidates[2], cur_dir)).as_posix()
    c3 = Path(os.path.relpath(candidates[3], cur_dir)).as_posix()
    my_set = {c0, c1, c2, c3}
    assert len(my_set) == 4
    assert 'resources/fakedir2/Game.agf' in my_set
    assert 'resources/fakedir2/fakedirA/Game.agf' in my_set
    assert 'resources/fakedir3/fakedir3/CopyGame/Game.agf' in my_set
    assert 'resources/otherfakedir/MinGame/Game.agf' in my_set


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
