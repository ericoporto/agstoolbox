from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem, QWidget, QLabel

from agstoolbox.at_icons import main_icon
from agstoolbox.core.ags.game_project import GameProject


class ProjectWidget(QWidget):
    project = None

    def __init__(self, ags_game_project: GameProject):
        QWidget.__init__(self)
        self.project = ags_game_project

        self.labelName = QLabel(self.project.name)

        self.labelVersion = QLabel(self.project.ags_editor_version)
        point_size = self.labelVersion.font().pointSize()
        point_size = round(point_size*0.75)
        self.labelVersion.font().setPointSize(point_size)

        self.labelDir = QLabel(self.project.directory)
        point_size = self.labelDir.font().pointSize()
        point_size = round(point_size*0.75)
        self.labelDir.font().setPointSize(point_size)

        top_hbox = QtWidgets.QHBoxLayout()
        bottom_hbox = QtWidgets.QHBoxLayout()
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(top_hbox)
        vbox.addLayout(bottom_hbox)
        top_hbox.addWidget(self.labelName)
        top_hbox.addWidget(self.labelVersion)
        bottom_hbox.addWidget(self.labelDir)
        self.setLayout(vbox)


class TreeItemProject(QTreeWidgetItem):
    itm_wdgt = None

    def __init__(self, ags_game_project: GameProject):
        QTreeWidgetItem.__init__(self)
        self.itm_wdgt = ProjectWidget(ags_game_project)

        self.setText(0, '')
        self.setIcon(0, main_icon())

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)
