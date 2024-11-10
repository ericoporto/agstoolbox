from __future__ import annotations  # for python 3.8

from typing import Final

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
