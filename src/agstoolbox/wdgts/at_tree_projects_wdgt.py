from __future__ import annotations  # for python 3.8
from operator import attrgetter
from typing import cast

from PyQt6.QtWidgets import QTreeWidget, QWidget, QFrame

from agstoolbox.at_tasks import do_update_projects
from agstoolbox.wdgts.at_tree_item_project import TreeItemProject
from agstoolbox.wdgts.at_tree_tools_wdgt import ToolsTree


class ProjectsTree(QTreeWidget):
    proj_update_task = None
    tools_tree: ToolsTree = None

    def __init__(self, parent: QWidget = None, toolsTree: ToolsTree = None):
        QTreeWidget.__init__(self, parent)

        self.tools_tree = toolsTree
        self.setHeaderHidden(True)
        self.setObjectName("treeProjects")
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setRootIsDecorated(False)
        self.setIndentation(0)

    # AGS Projects stuff
    def projects_schd_update(self):
        if self.proj_update_task is not None:
            return

        self.proj_update_task = do_update_projects(self.projects_update, self.projects_update_ended)

    def projects_update(self):
        self.clear()
        projs = self.proj_update_task.proj_list

        projs.sort(key=attrgetter("last_modified"), reverse=True)

        for p in projs:
            itm = TreeItemProject(ags_game_project=p)
            self.addTopLevelItem(itm)
            itm.updateInTree()

        self.projects_update_ended()

    def projects_update_ended(self):
        self.proj_update_task = None

    def filter(self, query: str):
        query = query.lower()
        non_empty_query: bool = query is not None and len(query) != 0
        root = self.invisibleRootItem()
        child_count = root.childCount()
        for i in range(child_count):
            hidden: bool = False
            item: TreeItemProject = cast(TreeItemProject, root.child(i))
            if non_empty_query:
                name: str = item.itm_wdgt.project.name
                name = name.lower()
                game_file: str = item.itm_wdgt.project.game_file
                game_file = game_file.lower()
                version_str: str = item.itm_wdgt.project.ags_editor_version.as_str
                hidden = not(query in name or query in game_file or query in version_str)

            item.setHidden(hidden)
