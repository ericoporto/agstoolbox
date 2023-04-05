#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime, timedelta

# TODO: fix to not need this (in Windows, MacOS and Linux)
if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.utils.time import internal_s_ago


def test_internal_s_ago_just_now():
    now = datetime.utcnow()
    diff = timedelta()
    assert internal_s_ago(now, diff) == "just now"


def test_internal_s_ago_minutes_ago():
    now = datetime.utcnow()
    t = now - timedelta(minutes=10)
    diff = now - t
    assert internal_s_ago(t, diff) == "10 minutes ago"


def test_internal_s_ago_hours_ago():
    now = datetime.utcnow()
    t = now - timedelta(hours=3)
    diff = now - t
    assert internal_s_ago(t, diff) == "3 hours ago"


def test_internal_s_ago_days_ago():
    now = datetime.utcnow()
    t = now - timedelta(days=2)
    diff = now - t
    assert internal_s_ago(t, diff) == "2 days ago"


def test_internal_s_ago_date_format():
    now = datetime.utcnow()
    t = now - timedelta(days=7)
    diff = now - t
    assert internal_s_ago(t, diff) == t.strftime("%d/%m/%Y")
