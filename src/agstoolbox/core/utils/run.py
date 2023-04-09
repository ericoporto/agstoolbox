from __future__ import annotations  # for python 3.8

import os
from subprocess import Popen

from agstoolbox.core.utils.file import get_file, get_dir


def run_exe_params(exe_path: str, params: list[str] = []):
    exe_file = get_file(exe_path)
    working_dir = get_dir(exe_path)

    p_params = [exe_file]
    p_params.extend(params)

    cwd = os.getcwd()
    os.chdir(working_dir)
    print('Popen: cwd=' + working_dir + ', ' + ' '.join(p_params))
    Popen(p_params, cwd=working_dir)
    os.chdir(cwd)
