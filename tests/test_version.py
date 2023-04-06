#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

if os.path.isdir(os.path.join(".", "src")) and os.path.isfile(os.path.join(".", "setup.py")):
    sys.path.append(os.path.realpath("src"))
    sys.path.append(os.path.realpath("src/agstoolbox"))

from agstoolbox.core.version.version_utils import tag_to_version_str, tag_to_family, \
    family_to_major, family_to_minor, \
    version_str_to_int, family_str_to_int, tag_to_version


def test_tag_to_version_str():
    assert tag_to_version_str("v.3.5.1.14") == "3.5.1.14"
    assert tag_to_version_str("v.3.  6.1.14") == "3.6.1.14"
    assert tag_to_version_str("v.4.0.0.14") == "4.0.0.14"
    assert tag_to_version_str("3.4.3.14") == "3.4.3.14"
    assert tag_to_version_str("version.3.3.1.14") == "3.3.1.14"
    assert tag_to_version_str("vivaldi.1") == "vivaldi.1"
    assert tag_to_version_str("v1.0.0.0") == "1.0.0.0"
    assert tag_to_version_str("version.1.2.3.4") == "1.2.3.4"
    assert tag_to_version_str("v1.2.3.4") == "1.2.3.4"
    assert tag_to_version_str("1.2.3.4") == "1.2.3.4"
    assert tag_to_version_str("v1.2.3") == "1.2.3.0"
    assert tag_to_version_str("1.2.3") == "1.2.3.0"
    assert tag_to_version_str("v1.2") == "1.2.0.0"
    assert tag_to_version_str("1.2") == "1.2.0.0"
    assert tag_to_version_str("v1") == "1.0.0.0"
    assert tag_to_version_str("1") == "1.0.0.0"
    assert tag_to_version_str("not.a.tag") == "not.a.tag"
    assert tag_to_version_str("") == ""


def test_tag_to_family():
    assert tag_to_family("v.3.5.1.14") == "3.5"
    assert tag_to_family("v.3.6.1.14") == "3.6"
    assert tag_to_family("v.4.0.0.14") == "4.0"
    assert tag_to_family("3.4.3.14") == "3.4"
    assert tag_to_family("3.3.1.14") == "3.3"
    assert tag_to_family("vivaldi.1") == "vivaldi.1"
    assert tag_to_family("v1.0.0.0") == "1.0"
    assert tag_to_family("version.1.2.3.4") == "1.2"
    assert tag_to_family("v1.2.3.4") == "1.2"
    assert tag_to_family("1.2.3.4") == "1.2"
    assert tag_to_family("v1.2.3") == "1.2"
    assert tag_to_family("1.2.3") == "1.2"
    assert tag_to_family("v1.2") == "1.2"
    assert tag_to_family("1.2") == "1.2"
    assert tag_to_family("v1") == "1.0"
    assert tag_to_family("1") == "1.0"
    assert tag_to_family("not.a.tag") == "not.a.tag"
    assert tag_to_family("") == ""


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


def test_version_str_to_int():
    assert version_str_to_int("v.3.5.1.14") == 3005001014
    assert version_str_to_int("v.3.  6.1.14") == 3006001014
    assert version_str_to_int("v.4.0.0.14") == 4000000014
    assert version_str_to_int("3.4.3.14") == 3004003014
    assert version_str_to_int("version.3.3.1.14") == 3003001014
    assert version_str_to_int("vivaldi.1") == -1


def test_family_str_to_int():
    assert family_str_to_int("3.5") == 3005000000
    assert family_str_to_int("3.6") == 3006000000
    assert family_str_to_int("4.0") == 4000000000
    assert family_str_to_int("3.4") == 3004000000
    assert family_str_to_int("3.3") == 3003000000
    assert family_str_to_int("vivaldi.1") == -1


def test_tag_to_version():
    v = tag_to_version("v.3.5.1.14")
    assert v.as_int == 3005001014
    assert v.major == "3"
    assert v.minor == "5"
    assert v.family == "3.5"
    assert v.family_as_int == 3005000000
