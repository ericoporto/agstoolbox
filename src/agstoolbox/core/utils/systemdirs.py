from __future__ import annotations  # for python 3.8

from pathlib import Path

from platformdirs import user_cache_dir, user_data_dir, user_log_dir, user_documents_dir


def get_user_cache_dir(app_name: str, app_author: str) -> str:
    return Path(user_cache_dir(app_name, app_author)).as_posix()


def get_user_data_dir(app_name: str, app_author: str) -> str:
    return Path(user_data_dir(app_name, app_author)).as_posix()


def get_user_log_dir(app_name: str, app_author: str) -> str:
    return Path(user_log_dir(app_name, app_author)).as_posix()


def get_user_documents_dir() -> str:
    return Path(user_documents_dir()).as_posix()
