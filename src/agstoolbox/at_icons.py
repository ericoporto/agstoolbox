from PyQt6 import QtGui

from agstoolbox import getdata


def main_icon() -> QtGui.QIcon:
    return QtGui.QIcon(getdata.path('at_icon.png'))


def main_icon_as_pixmap() -> QtGui.QPixmap:
    return QtGui.QPixmap(getdata.path('at_icon.png'))


def ags_editor_icon() -> QtGui.QIcon:
    return QtGui.QIcon(getdata.path('at_ags_editor_icon.png'))


def ags_editor_as_pixmap() -> QtGui.QPixmap:
    return QtGui.QPixmap(getdata.path('at_ags_editor_icon.png'))


def ags_engine_icon() -> QtGui.QIcon:
    return QtGui.QIcon(getdata.path('at_ags_engine_icon.png'))


def ags_engine_as_pixmap() -> QtGui.QPixmap:
    return QtGui.QPixmap(getdata.path('at_ags_engine_icon.png'))


def icon_refresh() -> QtGui.QIcon:
    return QtGui.QIcon(getdata.path('refresh_icon.png'))


def icon_exit() -> QtGui.QIcon:
    return QtGui.QIcon(getdata.path('exit_icon.png'))


def icon_settings() -> QtGui.QIcon:
    return QtGui.QIcon(getdata.path('settings_icon.png'))


def icon_refresh_as_pixmap() -> QtGui.QPixmap:
    return QtGui.QPixmap(getdata.path('refresh_icon.png'))


def icon_exit_as_pixmap() -> QtGui.QPixmap:
    return QtGui.QPixmap(getdata.path('exit_icon.png'))


def icon_settings_as_pixmap() -> QtGui.QPixmap:
    return QtGui.QPixmap(getdata.path('settings_icon.png'))
