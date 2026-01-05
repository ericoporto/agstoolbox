from __future__ import annotations  # for python 3.8

from typing import Final

from agstoolbox.core.version.version import Version

PROJECT_FILE_NAME: Final[str] = 'Game.agf'

COMPILED_LINUX_DIR_NAME: Final[str] = 'Linux'
COMPILED_WINDOWS_DIR_NAME: Final[str] = 'Windows'
COMPILED_WEB_DIR_NAME: Final[str] = 'Web'


class GameProject:
    """an AGS Game Project"""
    name: str | None = None
    game_file: str | None = None
    ags_editor_version: Version = None
    path: str | None = None
    directory: str | None = None
    encoding: str | None = None
    codepage: int | None = None
    last_modified = None
    ico_path = None
