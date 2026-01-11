from __future__ import annotations  # for python 3.8

from agstoolbox import __version__
from agstoolbox.core.gh.agstoolbox_release import AgsToolboxRelease
from agstoolbox.core.gh.agstoolbox_releases import list_agstoolbox_releases
from agstoolbox.core.version.version import Version
from agstoolbox.core.version.version_utils import tag_to_version


def get_latest_agstoolbox_release() -> AgsToolboxRelease | None:
    releases: list[AgsToolboxRelease] = list_agstoolbox_releases()
    if len(releases) >= 1:
        return releases[0]
    else:
        return None


def is_latest_agstoolbox_release() -> bool:
    # this should be cached somehow, as is it will always do a request
    agstoolbox_latest_release: AgsToolboxRelease | None = get_latest_agstoolbox_release()
    if agstoolbox_latest_release is None:
        return True # we have no idea, better pretend

    latest_version: Version = agstoolbox_latest_release.version
    executing_version: Version = tag_to_version(__version__)
    return latest_version.as_int == executing_version.as_int
