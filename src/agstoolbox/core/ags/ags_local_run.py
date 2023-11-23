from __future__ import annotations  # for python 3.8

import os
from subprocess import Popen

from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.utils.file import get_absolute_path
from agstoolbox.core.utils.run import run_exe_params


def ags_editor_start(editor: LocalAgsEditor, block: bool = False) -> int:
    return run_exe_params(editor.path, block)


def ags_editor_load(editor: LocalAgsEditor, project: GameProject, block: bool = False) -> int:
    project_path = get_absolute_path(project.path)
    return run_exe_params(editor.path, block, [project_path], )


def ags_editor_build(editor: LocalAgsEditor, project: GameProject, block: bool = False) -> int:
    project_path = get_absolute_path(project.path)
    return run_exe_params(editor.path, block, ['/compile', project_path])

