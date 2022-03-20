from __future__ import annotations  # for python 3.8
from PyQt6.QtCore import QThread
from PyQt6.QtCore import pyqtSignal as Signal

from agstoolbox.core.ags.get_local_ags_editors import list_ags_editors_in_dir_list
from agstoolbox.core.gh.download_release import download_release_to_cache
from agstoolbox.core.gh.install_release import install_release_from_cache
from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings import ConstSettings, Settings
from agstoolbox.core.ags.get_game_projects import list_game_projects_in_dir, \
    list_game_projects_in_dir_list
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
        self.proj_list = list_game_projects_in_dir_list(Settings().get_project_search_dirs())
        self.update_ended.emit()

    def stop(self):
        self.update_canceled.emit()


def do_update_projects(update_ended, update_canceled):
    thread = ProjUpdateThread()
    thread.update_ended.connect(update_ended)
    thread.update_canceled.connect(update_canceled)
    thread.start()
    return thread


class ToolsUpdateThreadDownloads(QThread):
    update_started = Signal()
    update_ended = Signal()
    update_canceled = Signal()
    tools_list = None

    def __init__(self):
        QThread.__init__(self)

    def run(self) -> None:
        self.update_started.emit()

        tools = list_releases()
        self.tools_list = tools
        self.update_ended.emit()

    def stop(self):
        self.update_canceled.emit()


def do_update_tools_downloads(update_ended, update_canceled):
    thread = ToolsUpdateThreadDownloads()
    thread.update_ended.connect(update_ended)
    thread.update_canceled.connect(update_canceled)
    thread.start()
    return thread


class ToolsUpdateThreadUnmanaged(QThread):
    update_started = Signal()
    update_ended = Signal()
    update_canceled = Signal()
    tools_list = None

    def __init__(self):
        QThread.__init__(self)

    def run(self) -> None:
        self.update_started.emit()
        self.tools_list = list_ags_editors_in_dir_list(
            Settings().get_manually_installed_editors_search_dirs())
        self.update_ended.emit()

    def stop(self):
        self.update_canceled.emit()


def do_update_tools_unmanaged(update_ended, update_canceled):
    thread = ToolsUpdateThreadUnmanaged()
    thread.update_ended.connect(update_ended)
    thread.update_canceled.connect(update_canceled)
    thread.start()
    return thread


class ToolsUpdateThreadManaged(QThread):
    update_started = Signal()
    update_ended = Signal()
    update_canceled = Signal()
    tools_list = None

    def __init__(self):
        QThread.__init__(self)

    def run(self) -> None:
        self.update_started.emit()
        self.tools_list = list_ags_editors_in_dir_list(
            list(Settings().get_tools_install_dir()))
        self.update_ended.emit()

    def stop(self):
        self.update_canceled.emit()


def do_update_tools_managed(update_ended, update_canceled):
    thread = ToolsUpdateThreadManaged()
    thread.update_ended.connect(update_ended)
    thread.update_canceled.connect(update_canceled)
    thread.start()
    return thread


# actual download
class DownloadAManagedToolThread(QThread):
    update_started = Signal()
    update_ended = Signal()
    release: Release = None

    def __init__(self, release: Release = None):
        QThread.__init__(self)
        self.release = release

    def run(self) -> None:
        self.update_started.emit()
        download_release_to_cache(self.release)
        install_release_from_cache(self.release)
        self.update_ended.emit()


def do_download_managed(release: Release, update_ended=None, update_started=None):
    thread = DownloadAManagedToolThread(release)
    if update_ended is not None:
        thread.update_ended.connect(update_ended)
    if update_started is not None:
        thread.update_started.connect(update_started)
    thread.start()
    return thread
