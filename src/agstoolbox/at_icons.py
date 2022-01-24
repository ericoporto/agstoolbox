from PyQt6 import QtGui

from agstoolbox import getdata


def main_icon():
    return QtGui.QIcon(QtGui.QPixmap(getdata.path('at_icon.png')))