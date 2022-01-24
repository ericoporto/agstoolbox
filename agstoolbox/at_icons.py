from PyQt6 import QtGui

from agstoolbox import getdata


def MainIcon():
    return QtGui.QPixmap(getdata.path('at_icon.png'))