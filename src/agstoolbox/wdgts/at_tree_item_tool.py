from __future__ import annotations  # for python 3.8
from enum import Enum
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTreeWidgetItem, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QWidget

from agstoolbox.at_icons import ags_editor_as_pixmap
from agstoolbox.at_tasks import do_download_managed
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.ags_local_run import start_ags_editor
from agstoolbox.core.utils.open_in_browser import open_in_browser
from agstoolbox.wdgts_utils.ags_local_extra import ags_editor_folder_in_explorer
from agstoolbox.core.gh.release import Release
from agstoolbox.core.utils.time import s_ago
from agstoolbox.wdgts_utils.action_utils import DefaultMenuQAction


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
        self.setWhatsThis(0, name)
        self.tool_type = tool_type
        self.setText(0, name)

    def __lt__(self, other):
        return False  # keeps unaltered when sorting

    def clear(self):
        for i in range(self.childCount()):
            self.removeChild(self.child(0))


# Tool Download Item
class TreeItemTool_Download_Widget(QWidget):
    release = None
    # we need to store the thread or the garbage collector will remove it!
    thread_download = None

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

    def install(self):
        if self.thread_download is not None:
            return
        self.thread_download = do_download_managed(self.release, self.download_ended)
        self.setEnabled(False)

    def show_gh_rel_page(self):
        open_in_browser(self.release.html_url)

    def mouseDoubleClickEvent(self, event):
        self.install()

    def download_ended(self):
        self.thread_download = None
        self.parent().parent().tools_schd_update_managed()
        self.setEnabled(True)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        install_action = DefaultMenuQAction(menu, "Install as managed Editor")
        show_gh_rel_page_action = menu.addAction("Show GitHub Release Page")
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == install_action:
            self.install()
        elif action == show_gh_rel_page_action:
            self.show_gh_rel_page()


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

    def open_editor(self):
        start_ags_editor(self.ags_editor)

    def mouseDoubleClickEvent(self, event):
        self.open_editor()

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        open_editor_action = DefaultMenuQAction(menu, "Open Editor")
        open_folder_action = menu.addAction("Open Folder in File Explorer")
        action = menu.exec(self.mapToGlobal(event.pos()))
        if action == open_editor_action:
            self.open_editor()
        elif action == open_folder_action:
            ags_editor_folder_in_explorer(self.ags_editor)


##################################################################################################
# item widgets

class TreeItemTool_Managed(QTreeWidgetItem):
    tool_type = ToolType.MANAGED_TOOL

    def __init__(self, parent: QTreeWidgetItem, ags_editor: LocalAgsEditor):
        QTreeWidgetItem.__init__(self, parent)
        self.itm_wdgt = TreeItemTool_Local_Widget(ags_editor, self.tool_type)

    def __lt__(self, other):
        return self.itm_wdgt.ags_editor.version.as_int < other.itm_wdgt.ags_editor.version.as_int

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)


class TreeItemTool_ExternallyInstalled(QTreeWidgetItem):
    tool_type = ToolType.EXTERNALLY_INSTALLED_TOOL

    def __init__(self, parent: QTreeWidgetItem, ags_editor: LocalAgsEditor):
        QTreeWidgetItem.__init__(self, parent)
        self.itm_wdgt = TreeItemTool_Local_Widget(ags_editor, self.tool_type)

    def __lt__(self, other):
        return self.itm_wdgt.ags_editor.version.as_int < other.itm_wdgt.ags_editor.version.as_int

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)


class TreeItemTool_Download(QTreeWidgetItem):
    tool_type = ToolType.AVAILABLE_TO_DOWNLOAD

    def __init__(self, parent: QTreeWidgetItem, release: Release):
        QTreeWidgetItem.__init__(self, parent)
        self.itm_wdgt = TreeItemTool_Download_Widget(release)

    def updateInTree(self):
        self.treeWidget().setItemWidget(self, 0, self.itm_wdgt)
