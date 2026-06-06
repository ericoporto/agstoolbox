from __future__ import annotations  # for python 3.8

import os
import sys

_gui_run: bool = False

def set_gui_run():
    global _gui_run
    _gui_run = True


def has_windows_console() -> bool:
    """
    Always return true on Linux, macOS, ...
    But we only return true on Windows if this is atbx ...
    """
    # note, I tried a few alternatives like checking pythonw, which fails in pyinstaller
    # I also tried kernel32.GetConsoleWindow(), but it seems it doesn't work in a few cases

    if os.name != "nt":
        return True  # POSIX: assume OK

    return not _gui_run
