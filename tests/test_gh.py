#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import os
import sys
from pathlib import Path

# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.gh.list_releases import parse_releases

cur_dir = Path(__file__).resolve().parent


def test_parse_releases():
    f = open(os.path.join(cur_dir, 'resources/gh_releases.json'))
    response_json = json.load(f)
    releases = parse_releases(response_json)
    assert len(releases) == 44
    assert releases[0].tag == "v.3.6.0.15"
    assert releases[1].tag == "v.3.6.0.14"
    assert releases[3].tag == "v.3.6.0.13"
    assert releases[3].name == "v.3.6.0.13 - Alpha 14"
    assert releases[3].url == "https://api.github.com/repos/adventuregamestudio/ags/releases/56166627"
    assert releases[3].archive_name == "AGS-3.6.0.13-Alpha14.zip"
    assert releases[3].archive_url == \
           "https://github.com/adventuregamestudio/ags/releases/download/v.3.6.0.13/AGS-3.6.0.13-Alpha14.zip"
    assert releases[3].archive_size == 25219327
