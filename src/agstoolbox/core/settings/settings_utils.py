from __future__ import annotations

import json
import os
from pathlib import Path
from platform import platform

from agstoolbox.core.settings.settings_data import SettingsData
from agstoolbox.core.utils.basics import get_str_list_from_dict, get_str_from_dict, \
    get_bool_from_dict


def load_settings_data_from_json_string(json_string: str) -> SettingsData:
    sd = SettingsData()

    if json_string is None:
        return sd

    try:
        data = json.loads(json_string)
    except ValueError:
        return sd

    if data is None:
        return sd

    sd.manually_installed_editors_search_dirs = get_str_list_from_dict(
        data, 'manually_installed_editors_search_dirs')
    sd.project_search_dirs = get_str_list_from_dict(
        data, 'project_search_dirs')
    sd.tools_install_dir = get_str_from_dict(
        data, 'tools_install_dir')
    sd.run_when_os_starts = get_bool_from_dict(
        data, 'run_when_os_starts')
    return sd


def save_settings_data_to_json_string(settings_data: SettingsData) -> str:
    data = {
        "tools_install_dir": settings_data.tools_install_dir,
        "project_search_dirs": settings_data.project_search_dirs,
        "manually_installed_editors_search_dirs":
            settings_data.manually_installed_editors_search_dirs,
        "run_when_os_starts": settings_data.run_when_os_starts
    }

    data = {k: v for k, v in data.items() if v is not None}

    json_string = json.dumps(data, indent=4, sort_keys=True) + "\n"
    return json_string


def win_get_default_editor_search_dirs():
    if not platform().lower().startswith('win'):
        return []

    versions = ['3.4.3', '3.5.0', '3.5.1', '3.6.0', '3.99.99', '3.99.100', '4.0.0']
    ret = []
    dirs = []
    p_files1 = os.environ["ProgramFiles"]
    p_files2 = os.environ["ProgramFiles(x86)"]
    p_files3 = os.environ["ProgramW6432"]
    if len(p_files1) > 1:
        dirs.append(p_files1)
    if len(p_files2) > 1:
        dirs.append(p_files2)
    if len(p_files3) > 1:
        dirs.append(p_files3)

    for v in versions:
        for d in dirs:
            ags_ed_d = os.path.join(d, 'Adventure Game Studio ' + v)
            if Path(ags_ed_d).exists():
                ret.append(ags_ed_d)

    ret = list(dict.fromkeys(ret))

    return ret
