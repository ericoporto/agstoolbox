from __future__ import annotations  # for python 3.8


class Version:
    def __init__(self):
        self.as_str: str = None
        self.as_ags4_str: str = None
        self.as_int: int = None
        self.series: str = None
        self.series_as_int: int = None
        self.family: str = None
        self.family_as_int: int = None
        self.major: str = None
        self.minor: str = None
        self.improv: str = None
        self.patch: str = None
