from __future__ import annotations  # for python 3.8

import os
from subprocess import Popen

from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.utils.file import get_absolute_path
from agstoolbox.core.utils.run import run_exe_params


def start_ags_editor(editor: LocalAgsEditor):
    run_exe_params(editor.path)


def ags_editor_load_project(editor: LocalAgsEditor, project: GameProject):
    project_path = get_absolute_path(project.path)
    run_exe_params(editor.path, [project_path])


def ags_editor_build_project(editor: LocalAgsEditor, project: GameProject):
    project_path = get_absolute_path(project.path)
    run_exe_params(editor.path, ['/compile', project_path])

