from __future__ import annotations  # for python 3.8

from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import QtGui

from agstoolbox import getdata
from agstoolbox.core.utils.singleton import Singleton


class StaticFontData:
    custom_fonts = {}
    parent: QApplication = None


class FontData(StaticFontData, metaclass=Singleton):
    pass


def add_font(font_id: str, filepath: str) -> None:
    if FontData.custom_fonts is None:
        FontData.custom_fonts = {}

    FontData.custom_fonts[font_id] = QtGui.QFontDatabase.addApplicationFont(getdata.path(filepath))


def set_custom_fonts(app: QApplication, main_widget: QWidget) -> None:
    FontData.parent = app
    FontData.custom_fonts = {}

    add_font('Beedii', "fonts/Beedii.ttf")


def get_custom_font_id(font_id: str) -> int:
    return FontData.custom_fonts[font_id]
