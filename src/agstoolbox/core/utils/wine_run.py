from __future__ import annotations  # for python 3.8

import os

from agstoolbox.core.utils.run import run_exe_params
from agstoolbox.core.utils.winepath import unix_path_to_wine_path


def wine_run_exe_params(exe_path: str, block: bool = False, timeout: int = 0,
                        param1: str = None,
                        param_path: str = None) -> int:
    wine_params = [exe_path]
    if param1 is not None:
        wine_params.append(param1)
    if param_path is not None:
        wine_project_path = unix_path_to_wine_path(param_path)
        wine_params.append(wine_project_path)

    wine_env = dict()
    wine_env['WINEDEBUG'] = '-all'
    wine_env['DXVK_LOG_LEVEL'] = 'warn'
    wine_env['MVK_CONFIG_LOG_LEVEL'] = '0'

    return run_exe_params('wine', block, timeout, wine_params, wine_env)
