from __future__ import annotations  # for python 3.8
from subprocess import Popen

from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.game_project import GameProject


def start_ags_editor(editor: LocalAgsEditor):
    Popen(editor.path)


def ags_editor_load_project(editor: LocalAgsEditor, project: GameProject):
    Popen([editor.path, project.path])
