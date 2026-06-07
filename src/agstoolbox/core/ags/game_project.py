from __future__ import annotations  # for python 3.8

from typing import Final

from agstoolbox.core.version.version import Version

PROJECT_FILE_NAME: Final[str] = 'Game.agf'

COMPILED_LINUX_DIR_NAME: Final[str] = 'Linux'
COMPILED_WINDOWS_DIR_NAME: Final[str] = 'Windows'
COMPILED_WEB_DIR_NAME: Final[str] = 'Web'


class GameProject:
    def __init__(self):
        """an AGS Game Project"""
        self.name: str | None = None
        self.game_file: str | None = None
        self.ags_editor_version: Version = None
        self.path: str | None = None
        self.directory: str | None = None
        self.encoding: str | None = None
        self.codepage: int | None = None
        self.last_modified = None
        self. ico_path = None
