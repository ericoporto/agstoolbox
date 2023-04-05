#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.utils.file import join_paths_as_posix
from agstoolbox.core.utils.pe import is_valid_exe, get_exe_information

cur_dir = str(Path(__file__).resolve().parent)

file_path01 = join_paths_as_posix(cur_dir, 'resources/fakedir1/AGSEditor.exe')
file_path02 = join_paths_as_posix(cur_dir, 'resources/fakedir2/fakedirA/AGSEditor.exe')
file_path03 = join_paths_as_posix(cur_dir, 'resources/fakedir3/fakedir3/CopyGame/Game.agf')
file_path04 = join_paths_as_posix(cur_dir, 'resources/otherfakedir/MinGame/Game.agf')


def test_is_valid_exe():
    assert is_valid_exe(file_path01) is True
    assert is_valid_exe(file_path02) is True
    assert is_valid_exe(file_path03) is False
    assert is_valid_exe(file_path04) is False


def test_get_exe_information():
    path01_exe_nfo = get_exe_information(file_path01)
    path02_exe_nfo = get_exe_information(file_path02)
    path03_exe_nfo = get_exe_information(file_path03)
    path04_exe_nfo = get_exe_information(file_path04)
    assert path01_exe_nfo.product_name == 'Made with Adventure Game Studio'
    assert path01_exe_nfo.internal_name == 'acwin'
    assert path01_exe_nfo.original_filename == 'acwin.exe'
    assert path02_exe_nfo.product_name == 'Adventure Game Studio'
    assert path02_exe_nfo.internal_name == 'AGSEditor.exe'
    assert path02_exe_nfo.original_filename == 'AGSEditor.exe'
    assert path03_exe_nfo.product_name is None
    assert path04_exe_nfo.product_name is None
