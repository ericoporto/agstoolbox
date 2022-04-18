from __future__ import annotations

import glob
import os
import shutil
from os.path import realpath
from os.path import dirname
from pathlib import Path


def get_dir(filepath):
    return Path(realpath(dirname(filepath))).as_posix()


def dir_is_valid(folderpath: str) -> bool:
    return folderpath is not None and \
           not "".__eq__(folderpath) and \
           Path(folderpath).exists() and \
           Path(folderpath).is_dir()


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


def get_gp_candidates_in_dir(directory: str, filename: str) -> list[str]:
    if not os.path.exists(directory):
        return []

    pathname = directory + "/**/" + filename
    files = glob.glob(pathname, recursive=True)
    return files


def join_paths_as_posix(path_first: str, path_second: str) -> str:
    return Path(os.path.join(path_first, path_second)).as_posix()


def remove_dir_contents(target_dir: str):
    try:
        with os.scandir(target_dir) as entries:
            for entry in entries:
                if entry.is_dir() and not entry.is_symlink():
                    shutil.rmtree(entry.path)
                elif entry.is_file():
                    os.remove(entry.path)
    except (FileNotFoundError, IOError):
        print("nothing to remove")


def mkdirp(path_dir: str):
    Path(path_dir).mkdir(parents=True, exist_ok=True)
