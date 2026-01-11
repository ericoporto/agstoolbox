from __future__ import annotations  # for python 3.8

from agstoolbox.core.version.version import Version


class AgsToolboxRelease:
    """a generic GitHub release object"""
    version: Version = None
    name = None
    url: str = None
    id: str = None
    tag: str = None

    html_url: str = None

    is_pre_release: bool = False
    text_details: str = None
    published_at: str = None
    published_at_timestamp: float = None
    winexe_name: str = None
    winexe_url: str = None
    winexe_size = None
    winexe_id: str = None
    winatbx_name: str = None
    winatbx_url: str = None
    winatbx_size = None
    winatbx_id: str = None
