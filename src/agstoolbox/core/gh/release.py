from agstoolbox.core.ags.ags_editor import AgsEditor


class Release(AgsEditor):
    """a GitHub release object"""
    url = None
    id = None
    tag = None

    html_url = None

    is_pre_release = False
    text_details = None
    published_at = None
    published_at_timestamp = None
    archive_name = None
    archive_url = None
    archive_size = None
    archive_id = None


