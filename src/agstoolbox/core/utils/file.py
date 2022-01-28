from os.path import realpath
from os.path import dirname
from pathlib import Path


def get_dir(filepath):
    return Path(realpath(dirname(filepath))).as_posix()
