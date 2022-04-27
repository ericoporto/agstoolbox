from __future__ import annotations

from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.utils.file import get_dir
from agstoolbox.wdgts_utils.file_explorer import open_folder


def ags_editor_folder_in_explorer(editor: LocalAgsEditor):
    open_folder(get_dir(editor.path))


def ags_project_folder_in_explorer(game_project: GameProject):
    open_folder(get_dir(game_project.path))
