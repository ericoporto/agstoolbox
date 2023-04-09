#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.utils.basics import get_str_list_from_dict, get_str_from_dict, \
    get_bool_from_dict


def test_get_str_list_from_dict():
    data = {"key1": ["value1", "value2"], "key2": "value3"}

    assert get_str_list_from_dict(data, "key1") == ["value1", "value2"]
    assert get_str_list_from_dict(data, "key2") == ["value3"]
    assert get_str_list_from_dict(data, "nonexistent_key") is None


def test_get_str_from_dict():
    data = {"key1": "value1", "key2": "value2"}

    assert get_str_from_dict(data, "key1") == "value1"
    assert get_str_from_dict(data, "key2") == "value2"
    assert get_str_from_dict(data, "nonexistent_key") is None


def test_get_bool_from_dict():
    data = {"key1": True, "key2": False, "key3": "some_value"}

    assert get_bool_from_dict(data, "key1") is True
    assert get_bool_from_dict(data, "key2") is False
    assert get_bool_from_dict(data, "key3") is True
    assert get_bool_from_dict(data, "nonexistent_key") is None

