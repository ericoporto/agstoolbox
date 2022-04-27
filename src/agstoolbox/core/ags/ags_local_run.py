from __future__ import annotations  # for python 3.8
from subprocess import Popen

from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.utils.file import get_dir
from agstoolbox.wdgts_utils.file_explorer import open_folder


def start_ags_editor(editor: LocalAgsEditor):
    Popen(editor.path)


def ags_editor_folder_in_explorer(editor: LocalAgsEditor):
    open_folder(get_dir(editor.path))


def ags_project_folder_in_explorer(game_project: GameProject):
    open_folder(get_dir(game_project.path))


def ags_editor_load_project(editor: LocalAgsEditor, project: GameProject):
    Popen([editor.path, project.path])
