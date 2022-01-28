#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(
        os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.gh.list_releases import tag_to_version, \
    tag_to_family, family_to_major, family_to_minor, parse_releases

cur_dir = Path(__file__).resolve().parent

def test_tag_to_version():
    assert tag_to_version("v.3.5.1.14") == "3.5.1.14"
    assert tag_to_version("v.3.  6.1.14") == "3.6.1.14"
    assert tag_to_version("v.4.0.0.14") == "4.0.0.14"
    assert tag_to_version("3.4.3.14") == "3.4.3.14"
    assert tag_to_version("version.3.3.1.14") == "3.3.1.14"
    assert tag_to_version("vivaldi.1") == "vivaldi.1"

def test_tag_to_family():
    assert tag_to_family("v.3.5.1.14") == "3.5"
    assert tag_to_family("v.3.6.1.14") == "3.6"
    assert tag_to_family("v.4.0.0.14") == "4.0"
    assert tag_to_family("3.4.3.14") == "3.4"
    assert tag_to_family("3.3.1.14") == "3.3"
    assert tag_to_family("vivaldi.1") == "vivaldi.1"


def test_family_to_major():
    assert family_to_major("3.4") == "3"
    assert family_to_major("3.7") == "3"
    assert family_to_major("4.4") == "4"
    assert family_to_major("73.4") == "73"
    assert family_to_major("experimental") == "experimental"


def test_family_to_minor():
    assert family_to_minor("3.4") == "4"
    assert family_to_minor("3.7") == "7"
    assert family_to_minor("4.2") == "2"
    assert family_to_minor("73.4") == "4"
    assert family_to_minor("experimental") == "experimental"


def test_parse_releases():
    f = open(os.path.join(cur_dir, 'resources/gh_releases.json'))
    response_json = json.load(f)
    releases = parse_releases(response_json)
    assert len(releases) == 30
    assert releases[0].tag == "v.3.6.0.15"
    assert releases[1].tag == "v.3.6.0.14"
    assert releases[2].tag == "v.3.6.0.13"
    assert releases[2].name == "v.3.6.0.13 - Alpha 14"
    assert releases[2].url == "https://api.github.com/repos/adventuregamestudio/ags/releases/56166627"
    assert releases[2].archive_name == "AGS-3.6.0.13-Alpha14.zip"
    assert releases[2].archive_url == \
           "https://github.com/adventuregamestudio/ags/releases/download/v.3.6.0.13/AGS-3.6.0.13-Alpha14.zip"
    assert releases[2].archive_size == 25219327
