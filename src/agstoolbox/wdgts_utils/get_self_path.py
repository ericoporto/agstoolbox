from __future__ import annotations

from PyQt6 import QtWidgets


def get_app_path() -> str:
    return QtWidgets.QApplication.applicationFilePath()
