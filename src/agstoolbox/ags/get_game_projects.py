import glob
import os.path
from os import PathLike
import defusedxml.ElementTree as ET

from agstoolbox.ags import game_project

PROJECT_FILE_NAME = 'Game.agf'
AGS_EDITOR_ROOT_TAG = 'AGSEditorDocument'


def get_gp_candidates_in_dir(directory: str) -> list[str]:
    pathname = directory + "/**/" + PROJECT_FILE_NAME
    files = glob.glob(pathname, recursive=True)
    return files


def is_game_file(filepath: str) -> bool:
    if not os.path.exists(filepath):
        return False

    if not filepath.endswith(PROJECT_FILE_NAME):
        return False

    # it's too big, may crash parser later, better ignor for now
    if os.path.getsize(filepath) > 268435456:
        return False

    platform = ''
    try:
        with open(filepath, 'r') as myfile:
            platform = myfile.read(4)
    except:
        return False
    finally:
        if not platform == '<?xml':
            return False

    tree = ET.parse(filepath)
    root = tree.getroot()
    if not root.tag == AGS_EDITOR_ROOT_TAG:
        return False

    if 'EditorVersion' not in root.attrib:
        return False

    return True


def gameagf_file_to_game_project(filepath: str) -> game_project:
    gp = game_project.GameProject()
    tree = ET.parse(filepath)
    root = tree.getroot()
    gp.path = filepath
    gp.name = root.find('Game/Settings/GameName').text
    gp.ags_editor_version = root['EditorVersion']
    gp.ags_editor_version_index = root['VersionIndex']
    return gp
