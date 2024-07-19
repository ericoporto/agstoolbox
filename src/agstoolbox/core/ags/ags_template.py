from __future__ import annotations  # for python 3.8

from typing import List
from pathlib import Path


def get_dir_file_list(directory: str, file_mask: str, search_option: str = 'top'):
    try:
        path = Path(directory)
        if search_option == 'top':
            return list(path.glob(file_mask))
        elif search_option == 'all':
            return list(path.rglob(file_mask))
    except IOError:
        return []


def add_matching_files(file_list: List[str], file_mask: str, parent_dir: str,
                       full_paths: bool = False, search_option: str = 'top'):
    files = get_dir_file_list(parent_dir, file_mask, search_option)
    if full_paths:
        file_list.extend([str(file) for file in files])
    else:
        file_list.extend([str(file.relative_to(parent_dir)) for file in files])


def construct_template_filelist(parent_dir: str) -> List[str]:
    files_to_include: List[str] = list()
    add_matching_files(files_to_include, "*.ico", parent_dir)
    add_matching_files(files_to_include, "Game.agf", parent_dir)
    add_matching_files(files_to_include, "acsprset.spr", parent_dir)
    add_matching_files(files_to_include, "preload.pcx", parent_dir)
    add_matching_files(files_to_include, "AudioCache/*.*", parent_dir)
    add_matching_files(files_to_include, "Speech/*.*", parent_dir)
    add_matching_files(files_to_include, "flic*.fl?", parent_dir)
    add_matching_files(files_to_include, "agsfnt*.ttf", parent_dir)
    add_matching_files(files_to_include, "agsfnt*.wfn", parent_dir)
    add_matching_files(files_to_include, "*.crm", parent_dir)
    add_matching_files(files_to_include, "*.asc", parent_dir)
    add_matching_files(files_to_include, "*.ash", parent_dir)
    add_matching_files(files_to_include, "*.txt", parent_dir)
    add_matching_files(files_to_include, "*.trs", parent_dir)
    add_matching_files(files_to_include, "*.pdf", parent_dir)
    add_matching_files(files_to_include, "*.ogv", parent_dir)
    return files_to_include
