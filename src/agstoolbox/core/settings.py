from __future__ import annotations  # for python 3.8

from platformdirs import user_cache_dir, user_data_dir, user_log_dir, user_documents_dir
import os
import json
from platform import platform
from pathlib import Path

from agstoolbox.core.utils.file import mkdirp, get_valid_dirs
from agstoolbox.core.utils.singleton import Singleton
from agstoolbox import __title__
from agstoolbox.core.utils.startup import remove_app_at_startup, set_app_at_startup
from agstoolbox.wdgts_utils.get_self_path import get_app_path

appname = __title__
appauthor = "eri0o"

SETTINGS_FILENAME = "settings.json"


def get_default_editor_search_dirs_in_windows():
    if not platform().lower().startswith('win'):
        return []

    versions = ['3.4.3', '3.5.0', '3.5.1', '3.6.0', '3.99.99', '3.99.100', '4.0.0']
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
    _run_when_os_starts: bool = False

    def set_manually_installed_editors_search_dirs(self, value: list[str]):
        if value is None:
            return

        self.manually_installed_editors_search_dirs = get_valid_dirs(value)

    def get_manually_installed_editors_search_dirs(self) -> list[str]:
        if type(self.manually_installed_editors_search_dirs) == type(list()):
            return get_valid_dirs(self.manually_installed_editors_search_dirs)

        return []

    def set_project_search_dirs(self, value: list[str]):
        if value is None:
            return

        self.project_search_dirs = get_valid_dirs(value)

    def get_project_search_dirs(self) -> list[str]:
        if type(self.project_search_dirs) == type(list()):
            return get_valid_dirs(self.project_search_dirs)

        return []

    def set_tools_install_dir(self, value):
        if value is None:
            return

        if not value == ConstSettings.DEFAULT_TOOLS_INSTALL_DIR:
            if not Path(value).exists():
                raise ValueError("Invalid path, doesn't exist")

        self.tools_install_dir = value
        self.editor_install_dir = Path(os.path.join(self.tools_install_dir, 'Editor')).as_posix()

    def set_run_when_os_starts(self, value: bool):
        if value is None:
            print("run_when_os_starts is None")

        if value is False:
            remove_app_at_startup(__title__)
            self._run_when_os_starts = False

        if value is True:
            self._run_when_os_starts = set_app_at_startup(__title__, get_app_path())

    def get_tools_install_dir(self):
        return self.tools_install_dir

    def get_editor_install_dir(self):
        return self.editor_install_dir

    def get_run_when_os_starts(self):
        return self._run_when_os_starts

    def save(self):
        settings_dir = get_settings_dir()
        settings_path = get_settings_path()

        mkdirp(settings_dir)

        data = {
            "tools_install_dir": self.tools_install_dir,
            "project_search_dirs": self.project_search_dirs,
            "manually_installed_editors_search_dirs": self.manually_installed_editors_search_dirs,
            "run_when_os_starts": self._run_when_os_starts
        }

        data_string = json.dumps(data, indent=4, sort_keys=True)

        with open(settings_path, 'w+') as f:
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

        mi_search_dirs = None
        try:
            mi_search_dirs = data['manually_installed_editors_search_dirs']
            if type(mi_search_dirs) == type(str()):
                mi_search_dirs = [mi_search_dirs]
        except KeyError:
            mi_search_dirs = None
        finally:
            if mi_search_dirs is not None:
                self.set_manually_installed_editors_search_dirs(mi_search_dirs)

        project_search_dirs = None
        try:
            project_search_dirs = data['project_search_dirs']
            if type(project_search_dirs) == type(str()):
                project_search_dirs = [project_search_dirs]
        except KeyError:
            project_search_dirs = None
        finally:
            if project_search_dirs is not None:
                self.set_project_search_dirs(project_search_dirs)

        tools_install_dir = None
        try:
            tools_install_dir = data['tools_install_dir']
        except KeyError:
            tools_install_dir = None
        finally:
            if tools_install_dir is not None:
                self.set_tools_install_dir(tools_install_dir)

        run_when_os_starts = None
        try:
            run_when_os_starts = data['run_when_os_starts']
        except KeyError:
            run_when_os_starts = None
        finally:
            if run_when_os_starts is not None:
                self.set_run_when_os_starts(run_when_os_starts)

    def __init__(self):
        self.load()


class Settings(BaseSettings, metaclass=Singleton):
    pass
