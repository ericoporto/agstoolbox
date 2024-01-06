from __future__ import annotations  # for python 3.8

from agstoolbox.core.ags.multifile import MultiFile


class MultiFileLib:
    data_file_names: list[str] | None = None
    files: list[MultiFile] | None = None
