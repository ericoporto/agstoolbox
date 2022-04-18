from __future__ import annotations  # for python 3.8
from subprocess import Popen

from agstoolbox.core.ags.ags_editor import LocalAgsEditor


def start_ags_editor(editor: LocalAgsEditor):
    Popen(editor.path)
