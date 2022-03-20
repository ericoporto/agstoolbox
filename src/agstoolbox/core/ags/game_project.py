from __future__ import annotations  # for python 3.8
from agstoolbox.core.version.version import Version

PROJECT_FILE_NAME = 'Game.agf'


class GameProject:
    """an AGS Game Project"""
    name = None
    ags_editor_version: Version = None
    ags_editor_version_index = None
    path = None
    directory = None
    last_modified = None
    ico_path = None
