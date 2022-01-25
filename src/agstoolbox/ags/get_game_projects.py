import glob
import os.path
from os import PathLike

from agstoolbox.ags import game_project

PROJECT_FILE_NAME = 'Game.agf'


def get_gp_candidates_in_dir(directory: str) -> list[str]:
    pathname = directory + "/**/" + PROJECT_FILE_NAME
    files = glob.glob(pathname, recursive=True)
    return files
