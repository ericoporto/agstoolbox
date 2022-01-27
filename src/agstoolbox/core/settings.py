from platformdirs import user_cache_dir, user_data_dir, user_log_dir, user_documents_dir
import os
from pathlib import Path

from agstoolbox.core.utils.singleton import Singleton
from agstoolbox import __title__


appname = __title__
appauthor = "eri0o"


class StaticSettings:
    double_click_interval = 400
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
