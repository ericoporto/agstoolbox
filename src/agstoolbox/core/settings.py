from __future__ import annotations  # for python 3.8
from platformdirs import user_cache_dir, user_data_dir, user_log_dir, user_documents_dir
import os
import json
from platform import platform
from pathlib import Path

from agstoolbox.core.utils.singleton import Singleton
from agstoolbox import __title__

appname = __title__
appauthor = "eri0o"

SETTINGS_FILENAME = "settings.json"


def get_default_editor_search_dirs_in_windows():
    if not platform().lower().startswith('win'):
        return []

    versions = ['3.4.3', '3.5.0', '3.5.1', '3.6.0', '3.9.9', '4.0.0']
    ret = []
    dirs = []
    p_files1 = os.environ["ProgramFiles"]
    p_files2 = os.environ["ProgramFiles(x86)"]
    p_files3 = os.environ["ProgramW6432"]
    if len(p_files1) > 1:
        dirs.append(p_files1)
    if len(p_files2) > 1:
        dirs.append(p_files2)
    if len(p_files3) > 1:
        dirs.append(p_files3)

    for v in versions:
        for d in dirs:
            ags_ed_d = os.path.join(d, 'Adventure Game Studio ' + v)
            if Path(ags_ed_d).exists():
                ret.append(ags_ed_d)

    ret = list(dict.fromkeys(ret))

    return ret


class StaticSettings:
    double_click_interval = 400
    DEFAULT_EXT_EDITORS_SEARCH_DIRS = get_default_editor_search_dirs_in_windows()

    cache_dir = Path(user_cache_dir(appname, appauthor)).as_posix()
    data_dir = Path(user_data_dir(appname, appauthor)).as_posix()
    log_dir = Path(user_log_dir(appname, appauthor)).as_posix()
    user_docs = Path(user_documents_dir()).as_posix()

    DEFAULT_TOOLS_INSTALL_DIR = Path(os.path.join(user_docs, 'AgsToolbox')).as_posix()
    DEFAULT_PROJECTS_SEARCH_DIRS = user_docs

    DEFAULT_MAIN_PANEL_WIDTH = 320
    DEFAULT_MAIN_PANEL_HEIGHT = 512


class ConstSettings(StaticSettings, metaclass=Singleton):
    pass


def get_settings_path():
    return os.path.join(ConstSettings().data_dir, SETTINGS_FILENAME)


class BaseSettings:
    agstoolbox_package_install = ConstSettings.DEFAULT_TOOLS_INSTALL_DIR
    editor_base_install_dir = Path(os.path.join(agstoolbox_package_install, 'Editor')).as_posix()
    manually_installed_editors_search_dirs = ConstSettings().DEFAULT_EXT_EDITORS_SEARCH_DIRS

    project_search_dirs = [ConstSettings().DEFAULT_PROJECTS_SEARCH_DIRS]
    editor_install_dir = editor_base_install_dir
    tools_install_dir = agstoolbox_package_install

    def set_manually_installed_editors_search_dirs(self, value: list[str]):
        if value is None:
            return

        self.manually_installed_editors_search_dirs = value

    def get_manually_installed_editors_search_dirs(self) -> list[str]:
        if type(self.manually_installed_editors_search_dirs) == type(list()):
            return self.manually_installed_editors_search_dirs

        return []

    def set_project_search_dirs(self, value: list[str]):
        if value is None:
            return

        self.project_search_dirs = value

    def get_project_search_dirs(self) -> list[str]:
        if type(self.project_search_dirs) == type(list()):
            return self.project_search_dirs

        return []

    def set_tools_install_dir(self, value):
        if value is None:
            return

        if not value == ConstSettings.DEFAULT_TOOLS_INSTALL_DIR:
            if not Path(value).exists():
                raise ValueError("Invalid path, doesn't exist")

        self.tools_install_dir = value
        self.editor_install_dir = Path(os.path.join(self.tools_install_dir, 'Editor')).as_posix()

    def get_tools_install_dir(self):
        return self.tools_install_dir

    def get_editor_install_dir(self):
        return self.editor_install_dir

    def save(self):
        Path(ConstSettings.data_dir).mkdir(parents=True, exist_ok=True)

        data = {
            "tools_install_dir": self.tools_install_dir,
            "manually_installed_editors_search_dirs": self.manually_installed_editors_search_dirs
        }

        data_string = json.dumps(data, indent=4, sort_keys=True)

        with open(get_settings_path(), 'w+') as f:
            f.write(data_string)

    def load(self):
        if not Path(get_settings_path()).exists():
            return

        data = None
        with open(get_settings_path(), 'r') as f:
            data_string = f.read()
            data = json.loads(data_string)

        if data is None:
            return

        mi = data['manually_installed_editors_search_dirs']
        if type(mi) == type(str()):
            mi = [mi]

        self.set_tools_install_dir(data['tools_install_dir'])
        self.set_manually_installed_editors_search_dirs(mi)

    def __init__(self):
        self.load()


class Settings(BaseSettings, metaclass=Singleton):
    pass
