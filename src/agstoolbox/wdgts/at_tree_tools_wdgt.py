from __future__ import annotations  # for python 3.8
from PyQt6.QtWidgets import QTreeWidget, QWidget, QAbstractScrollArea, QFrame

from agstoolbox.at_tasks import do_update_tools
from agstoolbox.wdgts.at_tree_item_tool import TreeItemTool


class ToolsTree(QTreeWidget):
    tool_update_task = None

    def __init__(self, parent: QWidget = None):
        QTreeWidget.__init__(self, parent)

        self.setHeaderHidden(True)
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.setObjectName("treeTools")
        self.setFrameStyle(QFrame.Shape.NoFrame)

    # Tool stuff
    def tools_schd_update(self):
        if self.tool_update_task is not None:
            return

        self.tool_update_task = do_update_tools(self.tools_update, self.tools_update_ended)

    def tools_update(self):
        self.clear()
        tools = self.tool_update_task.tools_list
        items = []
        for t in tools:
            itm = TreeItemTool(t)
            items.append(itm)

        self.addTopLevelItems(items)
        self.tools_update_ended()

    def tools_update_ended(self):
        self.tool_update_task = None
