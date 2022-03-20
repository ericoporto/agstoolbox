from __future__ import annotations  # for python 3.8
from enum import Enum
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget

from agstoolbox.at_icons import ags_editor_icon, ags_editor_as_pixmap
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.gh.release import Release
from agstoolbox.core.utils.time import s_ago


class ToolType(Enum):
    MANAGED_TOOL = 1
    AVAILABLE_TO_DOWNLOAD = 2
    EXTERNALLY_INSTALLED_TOOL = 3


class EditorImage(QLabel):
    def __init__(self, parent: QWidget = None):
        QLabel.__init__(self, parent)

        pxmap = ags_editor_as_pixmap()

        self.setPixmap(pxmap.scaled(
            32, 32,
            QtCore.Qt.AspectRatioMode.KeepAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation))
        self.setMaximumSize(32, 32)
        self.setMinimumSize(32, 32)


class TreeItemTool_Header(QTreeWidgetItem):
    name = None
    tool_type = None

    def __init__(self, name: str, tool_type: ToolType):
        QTreeWidgetItem.__init__(self)
        self.name = name
        self.tool_type = tool_type
        self.setText(0, name)

    def clear(self):
        for i in range(self.childCount()):
            self.removeChild(self.child(0))


# Tool Download Item
class TreeItemTool_Download_Widget(QWidget):
    release = None

    def __init__(self, release: Release, parent: QWidget = None):
        QWidget.__init__(self, parent)
        self.release = release

        self.icon_img = EditorImage()
        self.labelName = QLabel(self.release.name)
        self.labelName.setWordWrap(True)

        smaller_font = QtGui.QFont(
            self.labelName.font().family(),
            self.labelName.font().pointSize() * 0.90,
        )

        smallest_font = QtGui.QFont(
            self.labelName.font().family(),
            self.labelName.font().pointSize() * 0.75,
        )

        self.labelTime = QLabel(s_ago(self.release.published_at_timestamp))
        self.labelTime.setFont(smaller_font)
        self.labelTime.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.labelDir = QLabel(self.release.url)
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
        top_hbox.addLayout(right_vbox)
        bottom_hbox.addWidget(self.labelDir)

        main_qgrid = QGridLayout()
        main_qgrid.addWidget(self.icon_img)
        main_qgrid.addLayout(vbox, 0, 1)

        self.setLayout(main_qgrid)


# tool available locally for use
# either managed or unmanaged (externally installed)
class TreeItemTool_Local_Widget(QWidget):
    ags_editor = None

    def __init__(self, ags_editor: LocalAgsEditor, tool_type: ToolType, parent: QWidget = None):
        QWidget.__init__(self, parent)
        self.ags_editor = ags_editor

        self.icon_img = EditorImage()
        self.labelName = QLabel(self.ags_editor.name)
        self.labelName.setWordWrap(True)

        smaller_font = QtGui.QFont(
            self.labelName.font().family(),
            self.labelName.font().pointSize() * 0.90,
        )

        smallest_font = QtGui.QFont(
            self.labelName.font().family(),
            self.labelName.font().pointSize() * 0.75,
        )

        self.labelVersion = QLabel(self.ags_editor.version.as_str)
        self.labelVersion.setFont(smaller_font)
        self.labelVersion.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.labelTime = QLabel(s_ago(self.ags_editor.last_modified))
        self.labelTime.setFont(smaller_font)
        self.labelTime.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        self.labelDir = QLabel(self.ags_editor.path)
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


##################################################################################################
# item widgets

class TreeItemTool_Managed(QTreeWidgetItem):
    ags_editor = None
    tool_type = ToolType.MANAGED_TOOL

    def __init__(self, ags_editor: LocalAgsEditor):
        QTreeWidgetItem.__init__(self)
        self.itm_wdgt = TreeItemTool_Local_Widget(ags_editor, self.tool_type)

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)


class TreeItemTool_ExternallyInstalled(QTreeWidgetItem):
    local_editor = None
    tool_type = ToolType.EXTERNALLY_INSTALLED_TOOL

    def __init__(self, ags_editor: LocalAgsEditor):
        QTreeWidgetItem.__init__(self)
        self.itm_wdgt = TreeItemTool_Local_Widget(ags_editor, self.tool_type)

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)


class TreeItemTool_Download(QTreeWidgetItem):
    release = None
    tool_type = ToolType.AVAILABLE_TO_DOWNLOAD

    def __init__(self, release: Release):
        QTreeWidgetItem.__init__(self)
        self.itm_wdgt = TreeItemTool_Download_Widget(release)

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)
