from __future__ import annotations  # for python 3.8
import os
from operator import attrgetter

from agstoolbox.core.ags.ags_editor import EDITOR_FILE_NAME, LocalAgsEditor
from agstoolbox.core.ags.validate_ags_editor import validate_editor_exe
from agstoolbox.core.utils.file import get_gp_candidates_in_dir
from agstoolbox.core.utils.pe import is_valid_exe, get_exe_information
from agstoolbox.core.version.version_utils import version_str_to_version


def is_possibly_editor_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        return False

    if not filepath.endswith(EDITOR_FILE_NAME):
        return False

    if os.path.getsize(filepath) < 32768 or os.path.getsize(filepath) > 33554432:
        return False

    if not is_valid_exe(filepath):
        return False

    e = get_exe_information(filepath)

    if e.original_filename != 'AGSEditor.exe' or e.internal_name != 'AGSEditor.exe':
        return False

    if e.product_name != 'Adventure Game Studio':
        return False

    return True


def list_probable_ags_editors_paths_in_dir(filepath: str) -> list[str]:
    candidates = get_gp_candidates_in_dir(filepath, EDITOR_FILE_NAME)
    probable_candidates = []
    for c in candidates:
        if is_possibly_editor_file(c):
            probable_candidates.append(c)

    return probable_candidates


def list_probable_ags_editors_in_dir(filepath: str) -> list[LocalAgsEditor]:
    candidates = list_probable_ags_editors_paths_in_dir(filepath)

    editors = []
    for c in candidates:
        local_ae = LocalAgsEditor()
        pe_info = get_exe_information(c)
        version = version_str_to_version(pe_info.product_version)
        local_ae.version = version
        local_ae.path = c
        # TODO: skip validation until we can better maintain validation data
        # local_ae.validated = validate_editor_exe(c, version.as_str)
        local_ae.name = 'AGS Editor ' + version.as_str
        local_ae.last_modified = os.path.getmtime(filepath)
        editors.append(local_ae)

    unique = list(dict.fromkeys(editors))
    editors = unique
    editors.sort(key=attrgetter("last_modified"), reverse=True)

    return editors


def list_ags_editors_in_dir_list(filepaths: list[str]) -> list[LocalAgsEditor]:
    editors = []
    for path in filepaths:
        candidates = list_probable_ags_editors_in_dir(path)
        editors.extend(candidates)

    unique = list(dict.fromkeys(editors))
    editors = unique
    editors.sort(key=attrgetter("last_modified"), reverse=True)

    return editors
