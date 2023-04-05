#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
from pathlib import Path

if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.utils.file import get_gp_candidates_in_dir, get_unique_list, get_dir

cur_dir = Path(__file__).resolve().parent


def test_get_dir():
    f_path01 = os.path.join(cur_dir, 'resources/fakedir2/Game.agf')
    d_path01 = Path(os.path.join(cur_dir, 'resources/fakedir2')).as_posix()
    f_path02 = os.path.join(cur_dir, 'resources/fakedir2/fakedirA/Game.agf')
    d_path02 = Path(os.path.join(cur_dir, 'resources/fakedir2/fakedirA')).as_posix()
    f_path03 = os.path.join(cur_dir, 'resources/fakedir3/fakedir3/CopyGame/room1.asc')
    d_path03 = Path(os.path.join(cur_dir, 'resources/fakedir3/fakedir3/CopyGame')).as_posix()
    res01 = get_dir(f_path01)
    res02 = get_dir(f_path02)
    res03 = get_dir(f_path03)
    assert res01 == d_path01
    assert res02 == d_path02
    assert res03 == d_path03


def test_get_unique_list():
    # test no duplicates
    input_list: list[str] = ['apple', 'banana', 'orange']
    unique_list = get_unique_list(input_list)
    cmp_list: list[str] = input_list
    cmp_list.sort()
    unique_list.sort()
    assert unique_list == cmp_list

    # test with duplicates
    input_list = ['apple', 'banana', 'orange', 'apple', 'banana']
    unique_list = get_unique_list(input_list)
    cmp_list: list[str] = ['apple', 'banana', 'orange']
    cmp_list.sort()
    unique_list.sort()
    assert unique_list == cmp_list

    # test all duplicates
    input_list = ['apple', 'apple', 'apple', 'apple']
    unique_list = get_unique_list(input_list)
    cmp_list: list[str] = ['apple']
    cmp_list.sort()
    unique_list.sort()
    assert unique_list == cmp_list

    # test empty list
    input_list = []
    unique_list = get_unique_list(input_list)
    assert unique_list == []

    # test single element list
    input_list = ['apple']
    unique_list = get_unique_list(input_list)
    assert unique_list == input_list


def test_get_gp_candidates_in_dir():
    print(cur_dir.as_posix())
    candidates = get_gp_candidates_in_dir(cur_dir.as_posix(), 'Game.agf')
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
