import os
from os.path import realpath
from os.path import dirname
from pathlib import Path


def get_dir(filepath):
    return Path(realpath(dirname(filepath))).as_posix()


# TODO: do this non-hacky way!
def get_file_if_exists(directory: str, file: str):
    path_test_1 = os.path.join(directory, file.upper())
    path_test_2 = os.path.join(directory, file.lower())
    ftks = file.rsplit(".", 2)
    name = ftks[0]
    ext = ""
    if len(ftks) > 1:
        ext = ftks[1]

    path_test_3 = os.path.join(directory, name.upper() + "." + ext.lower())
    path_test_4 = os.path.join(directory, name.lower() + "." + ext.upper())

    if Path(path_test_1).exists():
        return path_test_1
    if Path(path_test_2).exists():
        return path_test_2
    if Path(path_test_3).exists():
        return path_test_3
    if Path(path_test_4).exists():
        return path_test_4

    return None
