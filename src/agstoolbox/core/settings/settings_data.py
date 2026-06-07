from __future__ import annotations  # for python 3.8

from typing import Final

SETTINGS_FILENAME: Final[str] = "settings.json"


class SettingsData:
    def __init__(self):
        self.run_when_os_starts: bool = None
        self.project_search_dirs: list[str] = None
        self.manually_installed_editors_search_dirs: list[str] = None
        self.tools_install_dir: str = None


