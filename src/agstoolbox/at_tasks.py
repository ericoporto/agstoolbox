from __future__ import annotations  # for python 3.8
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal as Signal

from agstoolbox.core.settings import ConstSettings
from agstoolbox.core.ags.get_game_projects import list_game_projects_in_dir
from agstoolbox.core.gh.list_releases import list_releases


class ProjUpdateThread(QThread):
    update_started = Signal()
    update_ended = Signal()
    update_canceled = Signal()
    proj_list = None

    def __init__(self):
        QThread.__init__(self)

    def run(self) -> None:
        self.update_started.emit()
        self.proj_list = list_game_projects_in_dir(ConstSettings.user_docs)
        self.update_ended.emit()

    def stop(self):
        self.update_canceled.emit()


def do_update_projects(update_ended, update_canceled):
    thread = ProjUpdateThread()
    thread.update_ended.connect(update_ended)
    thread.update_canceled.connect(update_canceled)
    thread.start()
    return thread


class ToolsUpdateThread(QThread):
    update_started = Signal()
    update_ended = Signal()
    update_canceled = Signal()
    tools_list = None

    def __init__(self):
        QThread.__init__(self)

    def run(self) -> None:
        self.update_started.emit()
        self.tools_list = list_releases()
        self.update_ended.emit()

    def stop(self):
        self.update_canceled.emit()


def do_update_tools(update_ended, update_canceled):
    thread = ToolsUpdateThread()
    thread.update_ended.connect(update_ended)
    thread.update_canceled.connect(update_canceled)
    thread.start()
    return thread
