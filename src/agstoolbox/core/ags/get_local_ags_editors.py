from __future__ import annotations  # for python 3.8
import os

from agstoolbox.core.ags.ags_editor import EDITOR_FILE_NAME
from agstoolbox.core.utils.pe import is_valid_exe, get_exe_information


def is_editor_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        return False

    if not filepath.endswith(EDITOR_FILE_NAME):
        return False

    if os.path.getsize(filepath) > 268435456 or os.path.getsize(filepath) < 2048:
        return False

    if not is_valid_exe(filepath):
        return False

    e = get_exe_information(filepath)

    if e.original_filename != 'AGSEditor.exe' or e.internal_name != 'AGSEditor.exe':
        return False

    if e.product_name != 'Adventure Game Studio':
        return False

    return True
