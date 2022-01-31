from __future__ import annotations  # for python 3.8
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem

from agstoolbox.at_icons import main_icon
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.gh.release import Release
from enum import Enum


class ToolType(Enum):
    MANAGED_TOOL = 1
    AVAILABLE_TO_DOWNLOAD = 2
    EXTERNALLY_INSTALLED_TOOL = 3


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


class TreeItemTool_Download(QTreeWidgetItem):
    release = None
    tool_type = ToolType.AVAILABLE_TO_DOWNLOAD

    def __init__(self, release: Release):
        QTreeWidgetItem.__init__(self)
        self.release = release

        self.setText(0, self.release.name)
        self.setIcon(0, main_icon())


class TreeItemTool_Managed(QTreeWidgetItem):
    release = None
    tool_type = ToolType.MANAGED_TOOL

    def __init__(self, release: Release):
        QTreeWidgetItem.__init__(self)
        self.release = release

        self.setText(0, self.release.name)
        self.setIcon(0, main_icon())


class TreeItemTool_ExternallyInstalled(QTreeWidgetItem):
    local_editor = None
    tool_type = ToolType.EXTERNALLY_INSTALLED_TOOL

    def __init__(self, local_editor: LocalAgsEditor):
        QTreeWidgetItem.__init__(self)
        self.local_editor = local_editor

        self.setText(0, self.local_editor.name)
        self.setIcon(0, main_icon())
