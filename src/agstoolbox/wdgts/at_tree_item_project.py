from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem

from agstoolbox.at_icons import main_icon
from agstoolbox.core.ags.game_project import GameProject


class TreeItemProject(QTreeWidgetItem):
    project = None

    def __init__(self, ags_game_project: GameProject):
        QTreeWidgetItem.__init__(self)
        self.project = ags_game_project

        self.setText(0, self.project.name)
        self.setIcon(0, main_icon())
