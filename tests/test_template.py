#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import List

from agstoolbox.core.ags.ags_template import construct_template_filelist

# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.utils.file import join_paths_as_posix

cur_dir = Path(__file__).resolve().parent
dir_path00 = join_paths_as_posix(cur_dir, 'resources/fakedir1')
dir_path01 = join_paths_as_posix(cur_dir, 'resources/fakedir2')
dir_path02 = join_paths_as_posix(cur_dir, 'resources/fakedir2/fakedirA')
dir_path03 = join_paths_as_posix(cur_dir, 'resources/fakedir3/fakedir3/CopyGame')
dir_path04 = join_paths_as_posix(cur_dir, 'resources/otherfakedir/MinGame')


def test_construct_template_filelist():
    filelist_0: List[str] = construct_template_filelist(dir_path00)
    assert filelist_0 is not None
    assert len(filelist_0) is 1
    assert 'Game.agf.txt' in filelist_0

    filelist_1: List[str] = construct_template_filelist(dir_path01)
    assert filelist_1 is not None
    assert len(filelist_1) == 1
    assert 'Game.agf' in filelist_1

    filelist_2: List[str] = construct_template_filelist(dir_path02)
    assert filelist_2 is not None
    assert len(filelist_2) == 2
    assert 'Game.agf' in filelist_2
    assert 'fake_file.txt' in filelist_2

    filelist_3: List[str] = construct_template_filelist(dir_path03)
    assert filelist_3 is not None
    assert len(filelist_3) == 11
    assert 'template.ico' in filelist_3
    assert 'Game.agf' in filelist_3
    assert 'acsprset.spr' in filelist_3
    assert 'AGSFNT0.WFN' in filelist_3
    assert 'AGSFNT1.WFN' in filelist_3
    assert 'AGSFNT2.WFN' in filelist_3
    assert 'room1.crm' in filelist_3
    assert 'GlobalScript.asc' in filelist_3
    assert 'room1.asc' in filelist_3
    assert 'GlobalScript.ash' in filelist_3
    assert 'template.txt' in filelist_3

    filelist_4: List[str] = construct_template_filelist(dir_path04)
    assert filelist_4 is not None
    assert len(filelist_4) == 11
    assert 'template.ico' in filelist_4
    assert 'Game.agf' in filelist_4
    assert 'acsprset.spr' in filelist_4
    assert 'AGSFNT0.WFN' in filelist_4
    assert 'AGSFNT1.WFN' in filelist_4
    assert 'AGSFNT2.WFN' in filelist_4
    assert 'room1.crm' in filelist_4
    assert 'GlobalScript.asc' in filelist_4
    assert 'room1.asc' in filelist_4
    assert 'GlobalScript.ash' in filelist_4
    assert 'template.txt' in filelist_4
