from __future__ import annotations  # for python 3.8


MODULE_FILE_SIGNATURE = b'AGSScriptModule\0'
MODULE_FILE_SECTION = 0xb4f76a65
MODULE_FILE_TRAILER = 0xb4f76a66


class ScriptModule:
    basename: str | None = None
    name: str | None = None
    version: str | None = None
    author: str | None = None
    description: str | None = None
    unique_key: str | None = None
    unique_key_int: int | None = None
    script: str | None = None
    header: str | None = None
