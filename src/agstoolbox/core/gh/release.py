from __future__ import annotations  # for python 3.8

from agstoolbox.core.ags.ags_editor import AgsEditor


class Release(AgsEditor):
    def __init__(self):
        """a GitHub release object"""
        self.url: str = None
        self.id: str = None
        self.tag: str = None

        self.html_url: str = None

        self.is_pre_release: bool = False
        self.text_details: str = None
        self.published_at: str = None
        self.published_at_timestamp: float = None
        self.archive_name: str = None
        self.archive_url: str = None
        self.archive_size = None
        self.archive_id: str = None


