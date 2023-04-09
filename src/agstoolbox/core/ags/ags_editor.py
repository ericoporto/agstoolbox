from __future__ import annotations  # for python 3.8
from agstoolbox.core.version.version import Version

EDITOR_FILE_NAME = 'AGSEditor.exe'


class AgsEditor:
    version: Version = None
    name = None


class LocalAgsEditor(AgsEditor):
    path = None
    externally_installed: bool = False
    validated = None
    last_modified = None
