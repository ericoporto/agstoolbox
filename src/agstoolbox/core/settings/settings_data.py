from __future__ import annotations  # for python 3.8

SETTINGS_FILENAME = "settings.json"


class SettingsData:
    run_when_os_starts: bool = None
    project_search_dirs: list[str] = None
    manually_installed_editors_search_dirs: list[str] = None
    tools_install_dir: str = None


