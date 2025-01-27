from __future__ import annotations  # for python 3.8

from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.utils.file import get_absolute_path
from agstoolbox.core.utils.run import run_exe_params


def ags_editor_start(editor: LocalAgsEditor, block: bool = False, timeout: int = 0) -> int:
    return run_exe_params(editor.path, block, timeout)


def ags_editor_load(editor: LocalAgsEditor, project: GameProject, block: bool = False, timeout: int = 0) -> int:
    project_path = get_absolute_path(project.path)
    return run_exe_params(editor.path, block, timeout, [project_path], )


def ags_editor_build(editor: LocalAgsEditor, project: GameProject, block: bool = False, timeout: int = 0) -> int:
    project_path = get_absolute_path(project.path)
    return run_exe_params(editor.path, block, timeout, ['/compile', project_path])


def ags_editor_template_build(editor: LocalAgsEditor, project: GameProject, block: bool = False, timeout: int = 0) -> int:
    project_path = get_absolute_path(project.path)
    return run_exe_params(editor.path, block, timeout, ['/maketemplate', project_path])
