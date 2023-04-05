from __future__ import annotations  # for python 3.8

from PyQt6 import QtCore
from PyQt6.QtWidgets import QTreeWidget, QWidget, QAbstractScrollArea, QFrame, QTreeWidgetItem

from agstoolbox.at_tasks import do_update_tools_downloads, do_update_tools_unmanaged, \
    do_update_tools_managed
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.ags_local_run import ags_editor_load_project
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.version.version import Version
from agstoolbox.wdgts.at_tree_item_tool import TreeItemTool_Header, ToolType, \
    TreeItemTool_Download, TreeItemTool_ExternallyInstalled, TreeItemTool_Managed


class ToolsTree(QTreeWidget):
    tool_update_downloads_task = None
    tool_update_unmanaged_task = None
    tool_update_managed_task = None
    header_managed = None
    header_download = None
    header_unmanaged = None
    managed_editors_list: list[LocalAgsEditor] = None
    unmanaged_editors_list: list[LocalAgsEditor] = None

    def __init__(self, parent: QWidget = None):
        QTreeWidget.__init__(self, parent)

        self.setHeaderHidden(True)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.setObjectName("treeTools")
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.clear()
        self.header_managed = TreeItemTool_Header(
            "Managed", ToolType.MANAGED_TOOL)
        self.header_unmanaged = TreeItemTool_Header(
            "Externally Installed", ToolType.EXTERNALLY_INSTALLED_TOOL)
        self.header_download = TreeItemTool_Header(
            "Available for Download", ToolType.AVAILABLE_TO_DOWNLOAD)
        self.addTopLevelItem(self.header_managed)
        self.addTopLevelItem(self.header_unmanaged)
        self.addTopLevelItem(self.header_download)
        self.setRootIsDecorated(False)
        self.setIndentation(0)

        # make headers expand or recover in a single click
        self.clicked.connect(self.toggleExpandSlot)
        self.itemExpanded.connect(self.itemIsExpanded)
        self.itemCollapsed.connect(self.itemIsCollapsed)

        self.header_managed.setExpanded(True)
        self.header_unmanaged.setExpanded(True)
        self.header_download.setExpanded(True)
        self.header_managed.setExpanded(False)
        self.header_unmanaged.setExpanded(False)

    def itemIsExpanded(self, itm: QTreeWidgetItem):
        itm.setText(0, "- " + itm.whatsThis(0))

    def itemIsCollapsed(self, itm: QTreeWidgetItem):
        itm.setText(0, "+ " + itm.whatsThis(0))

    def toggleExpandSlot(self, i):
        self.setExpanded(i, not self.isExpanded(i))

    ###############################################################################################
    # Download Tools stuff
    def tools_schd_update_downloads(self):
        if self.tool_update_downloads_task is not None:
            return

        self.tool_update_downloads_task = do_update_tools_downloads(
            self.tools_update_downloads, self.tools_update_downloads_ended)

    def tools_update_downloads(self):
        self.header_download.clear()
        tools = self.tool_update_downloads_task.tools_list

        if tools is not None:
            for t in tools:
                itm = TreeItemTool_Download(self.header_download, t)
                self.header_download.addChild(itm)
                itm.updateInTree()

        self.tools_update_downloads_ended()

    def tools_update_downloads_ended(self):
        self.tool_update_downloads_task = None

    ###############################################################################################

    ###############################################################################################
    # Unmanaged Tools stuff
    def tools_schd_update_unmanaged(self):
        if self.tool_update_unmanaged_task is not None:
            return

        self.tool_update_unmanaged_task = do_update_tools_unmanaged(
            self.tools_update_unmanaged, self.tools_update_unmanaged_ended)

    def tools_update_unmanaged(self):
        self.header_unmanaged.clear()
        tools = self.tool_update_unmanaged_task.tools_list
        tools.sort(key=lambda ed: ed.version.as_int, reverse=True)
        self.unmanaged_editors_list = tools

        if tools is not None:
            for t in tools:
                itm = TreeItemTool_ExternallyInstalled(self.header_unmanaged, t)
                self.header_unmanaged.addChild(itm)
                itm.updateInTree()

        self.tools_update_unmanaged_ended()

    def tools_update_unmanaged_ended(self):
        self.tool_update_unmanaged_task = None
        self.header_unmanaged.sortChildren(0, QtCore.Qt.SortOrder.DescendingOrder)

    ###############################################################################################

    ###############################################################################################
    # Managed Tools stuff
    def tools_schd_update_managed(self):
        if self.tool_update_managed_task is not None:
            return

        self.tool_update_managed_task = do_update_tools_managed(
            self.tools_update_managed, self.tools_update_managed_ended)

    def tools_update_managed(self):
        self.header_managed.clear()
        tools = self.tool_update_managed_task.tools_list
        tools.sort(key=lambda ed: ed.version.as_int, reverse=True)
        self.managed_editors_list = tools

        if tools is not None:
            for t in tools:
                itm = TreeItemTool_Managed(self.header_managed, t)
                self.header_managed.addChild(itm)
                itm.updateInTree()

        self.tools_update_managed_ended()

    def tools_update_managed_ended(self):
        self.tool_update_managed_task = None
        self.header_managed.sortChildren(0, QtCore.Qt.SortOrder.DescendingOrder)

    ###############################################################################################

    def open_project_tool(self, game_project: GameProject):
        project_version: Version = game_project.ags_editor_version

        for editor in self.managed_editors_list:
            if editor.version.as_int == project_version.as_int:
                ags_editor_load_project(editor, game_project)
                return

        for editor in self.unmanaged_editors_list:
            if editor.version.as_int == project_version.as_int:
                ags_editor_load_project(editor, game_project)
                return
