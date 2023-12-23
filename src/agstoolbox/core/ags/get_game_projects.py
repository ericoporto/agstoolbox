from __future__ import annotations  # for python 3.8
import os.path
from operator import attrgetter

import defusedxml.ElementTree as ETree

from agstoolbox.core.ags.game_project import GameProject, PROJECT_FILE_NAME
from agstoolbox.core.utils.file import get_dir, get_file_if_exists, get_gp_candidates_in_dir
from agstoolbox.core.version.version_utils import version_str_to_version

AGS_EDITOR_ROOT_TAG = 'AGSEditorDocument'


def text_file_starts_with_xml_Windows1252(filepath: str) -> bool:
    platform = ''
    try:
        with open(filepath, mode='r', encoding='cp1252') as file:
            platform = file.read(5)
    except FileNotFoundError:
        return False
    except OSError:
        return False
    finally:
        return platform == '<?xml'


def is_game_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        return False

    if not filepath.endswith(PROJECT_FILE_NAME):
        return False

    # it's too big, may crash parser later, better ignore for now
    if os.path.getsize(filepath) > 268435456:
        return False

    if not text_file_starts_with_xml_Windows1252(filepath):
        return False

    tree = ETree.parse(filepath)
    root = tree.getroot()
    if not root.tag == AGS_EDITOR_ROOT_TAG:
        return False

    if 'EditorVersion' not in root.attrib:
        return False

    return True


def gameagf_file_to_game_project(filepath: str) -> GameProject:
    gp = GameProject()
    tree = ETree.parse(filepath)
    root = tree.getroot()
    gp.path = filepath
    gp.directory = get_dir(filepath)
    ico_path = get_file_if_exists(gp.directory, "USER.ICO")
    if not ico_path:
        ico_path = get_file_if_exists(gp.directory, "template.ico")

    gp.ico_path = ico_path
    gp.last_modified = os.path.getmtime(filepath)

    gp.name = root.find('Game/Settings/GameName').text

    game_encoding = root.find('Game/Settings/GameTextEncoding')
    if game_encoding is not None:
        game_encoding = game_encoding.text
    [enc, codepage] = get_encoding_codepage(game_encoding)
    gp.encoding = enc
    gp.codepage = codepage

    game_file_name_htag = root.find('Game/Settings/GameFileName')
    if game_file_name_htag is not None:
        gp.game_file = game_file_name_htag.text
    else:
        gp.game_file = ""
    gp.ags_editor_version = version_str_to_version(root.attrib['EditorVersion'])
    gp.ags_editor_version_index = root.attrib['VersionIndex']
    return gp


def get_encoding_codepage(enc: str) -> [str, str]:
    codepage = 65001

    if enc is None:
        enc = 'utf-8'

    enc = enc.lower()
    if enc == '1252' or enc == 'ascii' or enc == 'ansi' or enc == 'windows-1252':
        enc = 'Windows-1252'
        codepage = 1252

    return [enc, codepage]


def valid_gameagf_file_to_game_project(filepath: str) -> GameProject | None:
    if is_game_file(filepath):
        return gameagf_file_to_game_project(filepath)
    else:
        return None


def list_game_projects_in_dir(filepath: str) -> list[GameProject]:
    candidates = get_gp_candidates_in_dir(filepath, PROJECT_FILE_NAME)
    ags_projects = []

    for candidate in candidates:
        if not is_game_file(candidate):
            continue

        ags_projects.append(gameagf_file_to_game_project(candidate))

    unique = list(dict.fromkeys(ags_projects))
    ags_projects = unique
    ags_projects.sort(key=attrgetter("last_modified"), reverse=True)

    return ags_projects


def list_game_projects_in_dir_list(filepaths: list[str]) -> list[GameProject]:
    ags_projects = []
    for path in filepaths:
        candidates = list_game_projects_in_dir(path)
        ags_projects.extend(candidates)

    unique = list(dict.fromkeys(ags_projects))
    ags_projects = unique
    ags_projects.sort(key=attrgetter("last_modified"), reverse=True)

    return ags_projects


def get_unique_game_project_in_path(project_path: str) -> GameProject | None:
    game_project: GameProject | None = valid_gameagf_file_to_game_project(project_path)

    if game_project is None:
        projects: list[GameProject] = list_game_projects_in_dir(project_path)
        if len(projects) != 1:
            print('WARN: Invalid project path, not exactly 1 game project found!')
            return None

        game_project = projects[0]

    return game_project
