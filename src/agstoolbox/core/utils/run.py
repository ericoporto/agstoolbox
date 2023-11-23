from __future__ import annotations  # for python 3.8

import os
from subprocess import Popen, TimeoutExpired

from agstoolbox.core.utils.file import get_file, get_dir


def run_exe_params(exe_path: str, block: bool = False, params=None) -> int:
    if params is None:
        params = []
    exe_file = get_file(exe_path)
    working_dir = get_dir(exe_path)

    p_params = [exe_file]
    p_params.extend(params)

    cwd = os.getcwd()
    os.chdir(working_dir)
    print('Popen: cwd=' + working_dir + ', ' + ' '.join(p_params))
    proc = Popen(p_params, cwd=working_dir, start_new_session=True)
    count = 0
    if block:
        while count < 1000:
            try:
                proc.wait(10)
            except TimeoutExpired:
                pass
            count += 1

        if count == 1000:
            proc.terminate()
    return_code: int = proc.returncode
    os.chdir(cwd)
    return return_code
