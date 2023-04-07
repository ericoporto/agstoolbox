#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.settings.settings_data import SettingsData
from agstoolbox.core.settings.settings_utils import load_settings_data_from_json_string, \
    save_settings_data_to_json_string


def test_load_json_string_empty():
    # Test that an empty JSON string returns the default SettingsData object
    json_string = ""
    result = load_settings_data_from_json_string(json_string)
    assert isinstance(result, SettingsData)
    assert not result.run_when_os_starts
    assert result.project_search_dirs is None
    assert result.manually_installed_editors_search_dirs is None
    assert result.tools_install_dir is None


def test_load_json_string_all_fields():
    # Test that a JSON string with all fields set returns the correct SettingsData object
    json_string = '{"run_when_os_starts": true, "project_search_dirs": ["dir1", "dir2"], ' \
                  '"manually_installed_editors_search_dirs": "dir3", "tools_install_dir": ' \
                  '"/usr/local/bin"} '
    result = load_settings_data_from_json_string(json_string)
    assert isinstance(result, SettingsData)
    assert result.run_when_os_starts
    assert result.project_search_dirs == ["dir1", "dir2"]
    assert result.manually_installed_editors_search_dirs == ["dir3"]
    assert result.tools_install_dir == "/usr/local/bin"


def test_load_json_string_missing_fields():
    # JSON string with missing fields returns a SettingsData obj with missing fields set to None
    json_string = '{"run_when_os_starts": false, "tools_install_dir": "/usr/local/bin"}'
    result = load_settings_data_from_json_string(json_string)
    assert isinstance(result, SettingsData)
    assert not result.run_when_os_starts
    assert result.project_search_dirs is None
    assert result.manually_installed_editors_search_dirs is None
    assert result.tools_install_dir == "/usr/local/bin"


def test_load_json_string_invalid_json():
    # Test that an invalid JSON string returns empty
    json_string = "not a valid JSON string"
    result = load_settings_data_from_json_string(json_string)
    assert not result.run_when_os_starts
    assert result.project_search_dirs is None
    assert result.manually_installed_editors_search_dirs is None
    assert result.tools_install_dir is None


# Tests for Saving the Json String

def test_save_settings_data_to_json_string_empty():
    # Test that the function returns an empty JSON string when given an empty SettingsData object
    settings_data = SettingsData()
    result = save_settings_data_to_json_string(settings_data)
    assert result == "{}\n"


def test_save_settings_data_to_json_string_all_fields():
    #  returns the correct JSON string when given a SettingsData object with all fields set
    settings_data = SettingsData()
    settings_data.run_when_os_starts = True
    settings_data.project_search_dirs = ["dir1", "dir2"]
    settings_data.manually_installed_editors_search_dirs = ["dir3"]
    settings_data.tools_install_dir = "/usr/local/bin"
    result = save_settings_data_to_json_string(settings_data)
    expected = \
        '{\n' \
        '    "manually_installed_editors_search_dirs": [\n' \
        '        "dir3"\n' \
        '    ],\n' \
        '    "project_search_dirs": [\n' \
        '        "dir1",\n' \
        '        "dir2"\n' \
        '    ],\n' \
        '    "run_when_os_starts": true,\n' \
        '    "tools_install_dir": "/usr/local/bin"\n' \
        '}\n'
    assert result == expected


def test_save_settings_data_to_json_string_missing_fields():
    # returns the correct JSON string when given a SettingsData object with some fields missing
    settings_data = SettingsData()
    settings_data.run_when_os_starts = False
    settings_data.tools_install_dir = "/usr/local/bin"
    result = save_settings_data_to_json_string(settings_data)
    expected = \
        '{\n' \
        '    "run_when_os_starts": false,\n' \
        '    "tools_install_dir": "/usr/local/bin"\n' \
        '}\n'
    assert result == expected
