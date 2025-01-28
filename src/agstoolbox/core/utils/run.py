from __future__ import annotations  # for python 3.8

import os
import sys
from subprocess import Popen, PIPE, TimeoutExpired

from agstoolbox.core.utils.file import get_file, get_dir
from agstoolbox.core.utils.pyinstaller_hacks import lock_dll_dir, unlock_dll_dir


def run_exe_params(exe_path: str, block: bool = False, timeout: int = 0, params=None) -> int:
    """
    Runs an executable file as a subprocess with optional blocking and timeout behavior.

    Args:
        exe_path (str): The path to the executable file to run.
        block (bool): If True, waits for the process to finish, respecting the timeout.
                      If False, the function returns immediately after starting the process.
        timeout (int): The maximum time to wait for the process to complete, in seconds.
                       If set to 0 or less, a default timeout of 10000 seconds is used.
                       Only valid when blocking.
        params (list, optional): Additional command-line parameters to pass to the executable.

    Returns:
        int: The return code of the process if it completes within the timeout.
             Returns -1 if the process is terminated due to exceeding the timeout.
    """
    if params is None:
        params = []

    exe_file = get_file(exe_path)
    working_dir = get_dir(exe_path)

    p_params = [exe_file]
    p_params.extend(params)

    # timeout is given in seconds
    if timeout <= 0:
        timeout = 10000

    cwd = os.getcwd()
    os.chdir(working_dir)
    lock_dll_dir()
    print('Popen: cwd=' + working_dir + ', ' + ' '.join(p_params))
    proc = Popen(p_params, cwd=working_dir, stdout=PIPE, stderr=PIPE, bufsize=1,
                 universal_newlines=True)

    timed_out: bool = False
    if block:
        try:
            # Wait for the process to complete or timeout
            outs, errs = proc.communicate(timeout=timeout)

            if outs:
                sys.stdout.write(outs)
            if errs:
                sys.stderr.write(errs)

        except TimeoutExpired:
            print("ERROR: Timeout time exceeded!")
            timed_out = True
        except Exception as e:
            print(f"ERROR: An exception occurred while running the process: {e}")
            timed_out = True

    return_code: int = proc.returncode
    if timed_out:
        proc.terminate()
        return_code = -1

    unlock_dll_dir()
    os.chdir(cwd)
    return return_code
