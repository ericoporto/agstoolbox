from PyQt6 import QtGui

from agstoolbox import getdata


def main_icon() -> QtGui.QIcon:
    return QtGui.QIcon(getdata.path('at_icon.png'))
