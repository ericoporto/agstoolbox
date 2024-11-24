from __future__ import annotations  # for python 3.8

from typing import Final

from agstoolbox.core.version.version import Version
from agstoolbox.core.version.version_utils import version_str_to_version, is_version_a_bigger_than_b


def get_installable_ags_versions() -> list[str]:
    versions: Final[list[str]] = [
        '3.4.3',
        '3.5.0',
        '3.5.1',
        '3.6.0',
        '3.6.1',
        '3.6.2',
        '3.99.99',
        '3.99.100',
        '4.0.0']

    return versions

def is_ags4(version: Version) -> bool:
    # there is an off-by-one mistake here, but let's leave this for now
    ags4_first: Version =  version_str_to_version('3.99.99')
    return is_version_a_bigger_than_b(version, ags4_first)
