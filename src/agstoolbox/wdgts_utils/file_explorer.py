from __future__ import annotations  # for python 3.8
import os

from PyQt6 import QtGui, QtCore


import subprocess
import sys


class UnsupportedPlatformException(Exception):
    pass


def _show_file_darwin(path):
    subprocess.check_call(["open", "--", path])


def _show_file_linux(path):
    subprocess.check_call(["xdg-open", "--", path])


def _show_file_win32(path):
    subprocess.check_call(["explorer", "/select", path])


def open_folder(path: str):
    _show_file_func = {'darwin': _show_file_darwin,
                       'linux': _show_file_linux,
                       'win32': _show_file_win32}
    fullpath = os.path.realpath(path)
    if not QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fullpath)):
        # failed
        try:
            show_file = _show_file_func[sys.platform](fullpath)
        except KeyError:
            raise UnsupportedPlatformException
