from __future__ import annotations  # for python 3.8


class MultiFile:
    def __init__(self):
        self.name: str | None = None
        self.filename: str | None = None
        self.datafile: int | None = None
        self.length: int | None = None
        self.offset: int | None = None
