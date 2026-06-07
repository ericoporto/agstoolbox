from __future__ import annotations  # for python 3.8

from agstoolbox.core.ags.multifile import MultiFile


class MultiFileLib:
    def __init__(self):
        self.data_file_names: list[str] | None = None
        self.files: list[MultiFile] | None = None
