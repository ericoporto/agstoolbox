from __future__ import annotations  # for python 3.8

import os

def has_windows_console() -> bool:
    if os.name != "nt":
        return True  # POSIX: assume OK

    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32

        # If this fails, there is no console
        return kernel32.GetConsoleWindow() != 0
    except Exception:
        return False
