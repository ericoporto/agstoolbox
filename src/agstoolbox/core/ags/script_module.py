from __future__ import annotations  # for python 3.8


MODULE_FILE_SIGNATURE = b'AGSScriptModule\0'
MODULE_FILE_SECTION = 0xb4f76a65
MODULE_FILE_TRAILER = 0xb4f76a66


class ScriptModule:
    def __init__(self):
        self.basename: str | None = None
        self.name: str | None = None
        self.version: str | None = None
        self.author: str | None = None
        self.description: str | None = None
        self.unique_key: str | None = None
        self.unique_key_int: int | None = None
        self.script: str | None = None
        self.header: str | None = None
