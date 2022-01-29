from __future__ import annotations  # for python 3.8
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QTransform

from agstoolbox.at_icons import main_icon_as_pixmap
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.utils.time import s_ago


class ProjectImage(QLabel):
    def __init__(self, img_icon_path: str, parent: QWidget = None):
        QLabel.__init__(self, parent)

        pxmap = main_icon_as_pixmap()
        if img_icon_path:
            pxmap = QtGui.QPixmap(img_icon_path)

        self.setPixmap(pxmap.scaled(
            32, 32,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation))
        self.setMaximumSize(32, 32)
        self.setMinimumSize(32, 32)


class ProjectWidget(QWidget):
    project = None

    def __init__(self, ags_game_project: GameProject, parent: QWidget = None):
        QWidget.__init__(self, parent)
        self.project = ags_game_project

        self.icon_img = ProjectImage(ags_game_project.ico_path)
        self.labelName = QLabel(self.project.name)
        self.labelName.setWordWrap(True)

        smaller_font = QtGui.QFont(
            self.labelName.font().family(),
            self.labelName.font().pointSize() * 0.90,
        )

        smallest_font = QtGui.QFont(
            self.labelName.font().family(),
            self.labelName.font().pointSize() * 0.75,
        )

        self.labelVersion = QLabel(self.project.ags_editor_version)
        self.labelVersion.setFont(smaller_font)
        self.labelVersion.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.labelTime = QLabel(s_ago(self.project.last_modified))
        self.labelTime.setFont(smaller_font)
        self.labelTime.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.labelDir = QLabel(self.project.directory)
        self.labelDir.setFont(smallest_font)
        self.labelDir.setDisabled(True)

        top_hbox = QHBoxLayout()
        bottom_hbox = QHBoxLayout()

        right_vbox = QVBoxLayout()

        vbox = QVBoxLayout()

        vbox.addLayout(top_hbox)
        vbox.addLayout(bottom_hbox)
        top_hbox.addWidget(self.labelName)
        right_vbox.addWidget(self.labelTime)
        right_vbox.addWidget(self.labelVersion)
        top_hbox.addLayout(right_vbox)
        bottom_hbox.addWidget(self.labelDir)

        main_qgrid = QGridLayout()
        main_qgrid.addWidget(self.icon_img)
        main_qgrid.addLayout(vbox, 0, 1)

        self.setLayout(main_qgrid)


class TreeItemProject(QTreeWidgetItem):
    itm_wdgt = None

    def __init__(self, ags_game_project: GameProject):
        QTreeWidgetItem.__init__(self)
        self.itm_wdgt = ProjectWidget(ags_game_project)

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)
