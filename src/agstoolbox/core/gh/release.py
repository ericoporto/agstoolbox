from __future__ import annotations  # for python 3.8

from agstoolbox.core.ags.ags_editor import AgsEditor


class Release(AgsEditor):
    """a GitHub release object"""
    url: str = None
    id: str = None
    tag: str = None

    html_url: str = None

    is_pre_release: bool = False
    text_details: str = None
    published_at: str = None
    published_at_timestamp: float = None
    archive_name: str = None
    archive_url: str = None
    archive_size = None
    archive_id: str = None


