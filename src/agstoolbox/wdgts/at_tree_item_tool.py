from __future__ import annotations  # for python 3.8
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem

from agstoolbox.at_icons import main_icon
from agstoolbox.core.gh.release import Release


class TreeItemTool(QTreeWidgetItem):
    release = None

    def __init__(self, release: Release):
        QTreeWidgetItem.__init__(self)
        self.release = release

        self.setText(0, self.release.name)
        self.setIcon(0, main_icon())
