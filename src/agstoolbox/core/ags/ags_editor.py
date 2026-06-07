from __future__ import annotations  # for python 3.8

from typing import Final

from agstoolbox.core.version.version import Version

EDITOR_FILE_NAME: Final[str] = 'AGSEditor.exe'


class AgsEditor:
    def __init__(self):
        self.version: Version = None
        self.name = None


class LocalAgsEditor(AgsEditor):
    def __init__(self):
        super().__init__()
        self.path = None
        self.externally_installed: bool = False
        self.validated = None
        self.last_modified = None
