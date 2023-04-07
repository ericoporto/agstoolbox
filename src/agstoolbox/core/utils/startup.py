from __future__ import annotations

import sys


def _win32_unsafe_remove_app_at_startup(app_name: str):
    from agstoolbox.core.utils.win_registry import set_run_key
    set_run_key(app_name, None)


def _win32_remove_app_at_startup(app_name: str):
    try:
        _win32_unsafe_remove_app_at_startup(app_name)
    except OSError:
        print("could not remove app from startup")


def _win32_set_app_at_startup(app_name: str, app_path: str) -> bool:
    from agstoolbox.core.utils.win_registry import set_run_key
    set_failed = False

    try:
        set_run_key(app_name, app_path)
    except OSError:
        set_failed = True

    if set_failed:
        try:
            _win32_unsafe_remove_app_at_startup(app_name)
        except OSError:
            set_failed = True

    return not set_failed


def _linux_remove_app_at_startup(app_name: str):
    print("stub _linux_remove_app_at_startup")


def _linux_set_app_at_startup(app_name: str, app_path: str) -> bool:
    print("stub _linux_set_app_at_startup")
    return False


def _darwin_remove_app_at_startup(app_name: str):
    print("stub _darwin_remove_app_at_startup")


def _darwin_set_app_at_startup(app_name: str, app_path: str) -> bool:
    print("stub _darwin_set_app_at_startup")
    return False


def remove_app_at_startup(app_name: str):
    _remove_app_at_startup = {
        'darwin': _darwin_remove_app_at_startup,
        'linux': _linux_remove_app_at_startup,
        'win32': _win32_remove_app_at_startup}

    _remove_app_at_startup[sys.platform](app_name)


def set_app_at_startup(app_name: str, app_path: str) -> bool:
    _set_app_at_startup = {
        'darwin': _darwin_set_app_at_startup,
        'linux': _linux_set_app_at_startup,
        'win32': _win32_set_app_at_startup}

    return _set_app_at_startup[sys.platform](app_name, app_path)
