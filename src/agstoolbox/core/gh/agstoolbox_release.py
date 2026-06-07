from __future__ import annotations  # for python 3.8

from agstoolbox.core.version.version import Version


class AgsToolboxRelease:
    def __init__(self):
        """a generic GitHub release object"""
        self.version: Version = None
        self.name = None
        self.url: str = None
        self.id: str = None
        self.tag: str = None

        self.html_url: str = None

        self.is_pre_release: bool = False
        self.text_details: str = None
        self.published_at: str = None
        self.published_at_timestamp: float = None
        self.winexe_name: str = None
        self.winexe_url: str = None
        self.winexe_size = None
        self.winexe_id: str = None
        self.winatbx_name: str = None
        self.winatbx_url: str = None
        self.winatbx_size = None
        self.winatbx_id: str = None
