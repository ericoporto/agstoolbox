from __future__ import annotations

import os

from agstoolbox.core.utils.win_registry import set_run_key, get_run_key


def _win_unsafe_remove_app_at_startup(app_name: str):
    set_run_key(app_name, None)


def _win_remove_app_at_startup(app_name: str):
    try:
        _win_unsafe_remove_app_at_startup(app_name)
    except OSError:
        print("could not remove app from startup")


def _win_set_app_at_startup(app_name: str, app_path: str) -> bool:
    set_failed = False

    try:
        set_run_key(app_name, app_path)
    except OSError:
        set_failed = True

    if set_failed:
        try:
            _win_unsafe_remove_app_at_startup(app_name)
        except OSError:
            set_failed = True
    else:
        set_path = get_run_key(app_name)
        set_failed = not set_path == app_path

    return not set_failed


def remove_app_at_startup(app_name: str):
    if os.name == 'nt':
        _win_remove_app_at_startup(app_name)


def set_app_at_startup(app_name: str, app_path: str) -> bool:
    if os.name == 'nt':
        return _win_set_app_at_startup(app_name, app_path)

    return False
