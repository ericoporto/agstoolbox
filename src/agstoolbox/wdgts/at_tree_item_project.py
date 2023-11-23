from __future__ import annotations  # for python 3.8
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout
from PyQt6.QtGui import QAction

from agstoolbox.at_icons import main_icon_as_pixmap
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.ags_local_run import ags_editor_load
from agstoolbox.wdgts_utils.ags_local_extra import ags_project_folder_in_explorer
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.utils.time import s_ago
from agstoolbox.wdgts_utils.action_utils import DefaultMenuQAction


class ActionEditorPair:
    action: QAction = None
    editor: LocalAgsEditor = None

    def __init__(self, action: QAction = None, editor: LocalAgsEditor = None):
        self.action = action
        self.editor = editor


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

        self.labelVersion = QLabel(self.project.ags_editor_version.as_str)
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

    def quick_open_project(self):
        self.parent().parent().tools_tree.open_project_tool(self.project)

    def quick_build_project(self):
        self.parent().parent().tools_tree.build_project_tool(self.project)

    def mouseDoubleClickEvent(self, event):
        self.quick_open_project()

    def get_managed_editors(self) -> list[LocalAgsEditor]:
        return self.parent().parent().tools_tree.managed_editors_list

    def get_unmanaged_editors(self) -> list[LocalAgsEditor]:
        return self.parent().parent().tools_tree.unmanaged_editors_list

    def set_managed_editors_menu(self,
                                 parent_menu: QtWidgets.QMenu = None) -> list[ActionEditorPair]:
        submenu = QtWidgets.QMenu("Open in Managed Editor", parent_menu)
        parent_menu.addMenu(submenu)
        editors = self.get_managed_editors()
        actions: list[ActionEditorPair] = list()
        for editor in editors:
            action = submenu.addAction(editor.name)
            actions.append(ActionEditorPair(action=action, editor=editor))

        return actions

    def set_unmanaged_editors_menu(self,
                                   parent_menu: QtWidgets.QMenu = None) -> list[ActionEditorPair]:
        submenu = QtWidgets.QMenu("Open in External Editor", parent_menu)
        parent_menu.addMenu(submenu)
        editors = self.get_unmanaged_editors()
        actions: list[ActionEditorPair] = list()
        for editor in editors:
            action = submenu.addAction(editor.name)
            actions.append(ActionEditorPair(action=action, editor=editor))

        return actions

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        quick_open_action = DefaultMenuQAction(menu, "Quick Open Project")
        quick_build_action = menu.addAction("Quick Build Project")
        open_folder_action = menu.addAction("Open Folder in File Explorer")
        menu.addSeparator()
        managed_actions = self.set_managed_editors_menu(menu)
        unmanaged_actions = self.set_unmanaged_editors_menu(menu)

        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == open_folder_action:
            ags_project_folder_in_explorer(self.project)
            return
        elif action == quick_open_action:
            self.quick_open_project()
            return
        elif action == quick_build_action:
            self.quick_build_project()
            return
        else:
            for a_pair in managed_actions:
                if a_pair.action == action:
                    ags_editor_load(a_pair.editor, self.project)
                    return

            for a_pair in unmanaged_actions:
                if a_pair.action == action:
                    ags_editor_load(a_pair.editor, self.project)
                    return


class TreeItemProject(QTreeWidgetItem):
    itm_wdgt = None

    def __init__(self, ags_game_project: GameProject):
        QTreeWidgetItem.__init__(self)
        self.itm_wdgt = ProjectWidget(ags_game_project)

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)
