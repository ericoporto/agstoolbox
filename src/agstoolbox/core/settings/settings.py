from __future__ import annotations  # for python 3.8

import os
from pathlib import Path

from agstoolbox.core.settings.settings_data import SETTINGS_FILENAME, SettingsData
from agstoolbox.core.settings.settings_utils import load_settings_data_from_json_string, \
    save_settings_data_to_json_string, win_get_default_editor_search_dirs
from agstoolbox.core.utils.file import mkdirp, get_unique_valid_dirs
from agstoolbox.core.utils.singleton import Singleton
from agstoolbox import __title__
from agstoolbox.core.utils.startup import remove_app_at_startup, set_app_at_startup
from agstoolbox.core.utils.systemdirs import get_user_cache_dir, get_user_data_dir, \
    get_user_log_dir, get_user_documents_dir

app_name = __title__
app_author = "eri0o"


class StaticSettings:
    double_click_interval = 400
    DEFAULT_EXT_EDITORS_SEARCH_DIRS = win_get_default_editor_search_dirs()

    cache_dir = get_user_cache_dir(app_name, app_author)
    data_dir = get_user_data_dir(app_name, app_author)
    log_dir = get_user_log_dir(app_name, app_author)
    user_docs = get_user_documents_dir()

    DEFAULT_TOOLS_INSTALL_DIR = Path(os.path.join(user_docs, 'AgsToolbox')).as_posix()
    DEFAULT_PROJECTS_SEARCH_DIRS = [user_docs]

    DEFAULT_MAIN_PANEL_WIDTH = 320
    DEFAULT_MAIN_PANEL_HEIGHT = 512


class ConstSettings(StaticSettings, metaclass=Singleton):
    pass


def get_settings_dir():
    return Path(ConstSettings().data_dir).as_posix()


def get_settings_path():
    return Path(
        os.path.join(os.path.abspath(ConstSettings().data_dir), SETTINGS_FILENAME)).as_posix()


class BaseSettings:
    agstoolbox_package_install = ConstSettings.DEFAULT_TOOLS_INSTALL_DIR
    editor_base_install_dir = Path(os.path.join(agstoolbox_package_install, 'Editor')).as_posix()
    manually_installed_editors_search_dirs = ConstSettings().DEFAULT_EXT_EDITORS_SEARCH_DIRS

    project_search_dirs = ConstSettings().DEFAULT_PROJECTS_SEARCH_DIRS
    editor_install_dir = editor_base_install_dir
    tools_install_dir = agstoolbox_package_install
    run_when_os_starts: bool = False
    app_path: str = ""

    def set_app_path(self, path: str):
        self.app_path = path

    def set_manually_installed_editors_search_dirs(self, value: list[str]):
        if value is None:
            return

        self.manually_installed_editors_search_dirs = get_unique_valid_dirs(value)

    def get_manually_installed_editors_search_dirs(self) -> list[str]:
        if type(self.manually_installed_editors_search_dirs) == type(list()):
            return get_unique_valid_dirs(self.manually_installed_editors_search_dirs)

        return []

    def set_project_search_dirs(self, value: list[str]):
        if value is None:
            return

        self.project_search_dirs = get_unique_valid_dirs(value)

    def get_project_search_dirs(self) -> list[str]:
        if type(self.project_search_dirs) == type(list()):
            return get_unique_valid_dirs(self.project_search_dirs)

        return []

    def set_tools_install_dir(self, value):
        if value is None:
            return

        if value == "":
            value = ConstSettings.DEFAULT_TOOLS_INSTALL_DIR

        if not value == ConstSettings.DEFAULT_TOOLS_INSTALL_DIR:
            if not Path(value).exists():
                raise ValueError("Invalid path, doesn't exist")

        self.tools_install_dir = value
        self.editor_install_dir = Path(os.path.join(self.tools_install_dir, 'Editor')).as_posix()

    def set_run_when_os_starts(self, value: bool):
        if value is None or self.app_path is None or self.app_path == "":
            return

        if value is False:
            remove_app_at_startup(__title__)
            self.run_when_os_starts = False

        if value is True and self.app_path is not None and self.app_path != "":
            self.run_when_os_starts = set_app_at_startup(__title__, self.app_path)

    def get_tools_install_dir(self):
        return self.tools_install_dir

    def get_editor_install_dir(self):
        return self.editor_install_dir

    def get_run_when_os_starts(self):
        return self.run_when_os_starts

    def dump(self) -> str:
        data = SettingsData()
        data.run_when_os_starts = self.run_when_os_starts
        data.project_search_dirs = self.project_search_dirs
        data.manually_installed_editors_search_dirs = self.manually_installed_editors_search_dirs
        data.tools_install_dir = self.tools_install_dir

        return save_settings_data_to_json_string(data)

    def save(self):
        settings_dir = get_settings_dir()
        settings_path = get_settings_path()

        mkdirp(settings_dir)
        data_string: str = self.dump()

        with open(settings_path, 'w+', encoding="utf-8") as f:
            f.write(data_string)
            f.flush()

    def load(self):
        settings_path: str = get_settings_path()
        if not Path(settings_path).exists():
            return

        data = None
        sd = None
        with open(settings_path, 'r', encoding="utf-8") as f:
            data_string = f.read()
            if data_string is None:
                return
            sd = load_settings_data_from_json_string(data_string)

        self.set_manually_installed_editors_search_dirs(sd.manually_installed_editors_search_dirs)
        self.set_project_search_dirs(sd.project_search_dirs)
        self.set_tools_install_dir(sd.tools_install_dir)
        self.set_run_when_os_starts(sd.run_when_os_starts)

    def __init__(self):
        self.load()


class Settings(BaseSettings, metaclass=Singleton):
    pass
