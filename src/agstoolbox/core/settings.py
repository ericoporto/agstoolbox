from platformdirs import user_cache_dir, user_data_dir, user_log_dir, user_documents_dir
import os
from platform import platform
from pathlib import Path

from agstoolbox.core.utils.singleton import Singleton
from agstoolbox import __title__


appname = __title__
appauthor = "eri0o"


def get_default_search_dirs_in_windows():
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
            ret.append(os.path.join(d, 'Adventure Game Studio ' + v))

    return ret


class StaticSettings:
    double_click_interval = 400
    MANUALLY_INSTALLED_SEARCH_DIRS = get_default_search_dirs_in_windows()

    cache_dir = Path(user_cache_dir(appname, appauthor)).as_posix()
    data_dir = Path(user_data_dir(appname, appauthor)).as_posix()
    log_dir = Path(user_log_dir(appname, appauthor)).as_posix()
    user_docs = Path(user_documents_dir()).as_posix()
    DEFAULT_MAIN_PANEL_WIDTH = 320
    DEFAULT_MAIN_PANEL_HEIGHT = 512


class ConstSettings(StaticSettings, metaclass=Singleton):
    pass


class BaseSettings:
    agstoolbox_package_install = Path(os.path.join(ConstSettings.user_docs, 'AgsToolbox')).as_posix()
    editor_base_install_dirs = Path(os.path.join(agstoolbox_package_install, 'Editor')).as_posix()

    tools_install_dir = None

    def set_tools_install_dir(self, value):
        self.tools_install_dir = value

    def get_tools_install_dir(self):
        return self.tools_install_dir

    def get_agstoolbox_package_install(self):
        return self.agstoolbox_package_install

    def get_editor_base_install_dirs(self):
        return self.editor_base_install_dirs


class Settings(BaseSettings, metaclass=Singleton):
    pass
