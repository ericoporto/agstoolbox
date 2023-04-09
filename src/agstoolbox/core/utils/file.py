from __future__ import annotations

import errno
import glob
import os
import shutil
from os.path import realpath
from os.path import dirname
from os.path import join as join_paths
from pathlib import Path


def get_dir(filepath: str):
    return Path(realpath(dirname(filepath))).as_posix()


def get_file(filepath: str):
    return os.path.basename(Path(filepath).as_posix())


def get_absolute_path(filepath: str) -> str:
    return os.path.abspath(os.path.expanduser(os.path.expandvars(filepath)))


def dir_is_valid(folderpath: str) -> bool:
    res: bool = False
    try:
        res = folderpath is not None and \
              not "".__eq__(folderpath) and \
              Path(folderpath).exists() and \
              Path(folderpath).is_dir()
    except Exception as e:
        res = False
    finally:
        return res


def get_valid_dirs(directories: list[str]) -> list[str]:
    return [d for d in directories if dir_is_valid(d)]


def get_unique_list(lst: list[str]) -> list[str]:
    return list(dict.fromkeys(lst))


def get_unique_valid_dirs(directories: list[str]) -> list[str]:
    return get_valid_dirs(get_unique_list(directories))


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


def internal_run_fast_scandir(directory: str, filename: str):  # dir: str, ext: list
    sub_folders, files = [], []

    if Path(directory).is_dir() and Path(directory).exists():
        directory = Path(directory).as_posix()
    else:
        directory = get_dir(directory)

    os_scandir_res = []
    try:
        os_scandir_res = os.scandir(directory)
    except NotADirectoryError:
        os_scandir_res = []
    except PermissionError:
        os_scandir_res = []

    for f in os_scandir_res:
        if f.is_dir():
            sub_folders.append(f.path)
        if f.is_file():
            if f.name == filename:
                files.append(f.path)

    for s_dir in list(sub_folders):
        sf, f = internal_run_fast_scandir(s_dir, filename)
        sub_folders.extend(sf)
        files.extend(f)
    return sub_folders, files


def get_gp_candidates_in_dir_fastscandir(directory: str, filename: str) -> list[str]:
    # in Python 3.8, this is ~25% faster, but python 3.10 it's slower
    # unfortunately, we are using Python 3.8 for the time being
    _, files = internal_run_fast_scandir(directory, filename)
    return files


def get_gp_candidates_in_dir_glob(directory: str, filename: str) -> list[str]:
    pathname = directory + "/**/" + filename
    return glob.glob(pathname, recursive=True)


def get_gp_candidates_in_dir(directory: str, filename: str) -> list[str]:
    if not os.path.exists(directory):
        return []

    files = get_gp_candidates_in_dir_fastscandir(directory, filename)
    if not files:
        return []

    files = [Path(f).as_posix() for f in files]

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
        # print("nothing to remove")
        pass


def _mk_dir_recursive(dir_path):
    if os.path.isdir(dir_path):
        return
    h, t = os.path.split(dir_path)  # head/tail
    if not os.path.isdir(h):
        _mk_dir_recursive(h)

    new_path = join_paths(h, t)
    if not os.path.isdir(new_path):
        try:
            os.mkdir(str(new_path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
            pass


def mkdirp(path_dir: str):
    _mk_dir_recursive(path_dir)
    # alternate implementation if needed
    # Path(path_dir).mkdir(parents=True, exist_ok=True)
