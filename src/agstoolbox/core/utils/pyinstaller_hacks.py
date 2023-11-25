from __future__ import annotations

import os
import sys


def is_running_from_pyinstaller() -> bool:
    return getattr(sys, 'frozen', False) is not False


def get_extracted_path() -> str:
    if hasattr(sys, '_MEIPASS'):
        return str(os.path.join(sys._MEIPASS))  # pylint: disable=no-member
    else:
        return str("")


def _win32_requires_dll_locking() -> bool:
    if is_running_from_pyinstaller():
        ext_path: str = get_extracted_path()
        return len(ext_path) > 0
    else:
        return False


def _do_nothing():
    pass


def _win32_lock_dll_dir():
    if _win32_requires_dll_locking():
        import ctypes
        ctypes.windll.kernel32.SetDllDirectoryW(None)


def _win32_unlock_dll_dir():
    if _win32_requires_dll_locking():
        import ctypes
        ctypes.windll.kernel32.SetDllDirectoryW(get_extracted_path())


def lock_dll_dir():
    _lock_dll_dir = {
        'darwin': _do_nothing,
        'linux': _do_nothing,
        'win32': _win32_lock_dll_dir}

    _lock_dll_dir[sys.platform]()


def unlock_dll_dir():
    _unlock_dll_dir = {
        'darwin': _do_nothing,
        'linux': _do_nothing,
        'win32': _win32_unlock_dll_dir}

    _unlock_dll_dir[sys.platform]()
