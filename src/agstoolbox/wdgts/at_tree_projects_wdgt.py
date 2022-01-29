from operator import attrgetter

from PyQt6.QtWidgets import QTreeWidget, QWidget, QFrame

from agstoolbox.at_tasks import do_update_projects
from agstoolbox.wdgts.at_tree_item_project import TreeItemProject


class ProjectsTree(QTreeWidget):
    proj_update_task = None

    def __init__(self, parent: QWidget = None):
        QTreeWidget.__init__(self, parent)

        self.setHeaderHidden(True)
        self.setObjectName("treeProjects")
        self.setFrameStyle(QFrame.Shape.NoFrame)

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
