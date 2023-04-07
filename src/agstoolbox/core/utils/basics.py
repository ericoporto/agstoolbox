from __future__ import annotations  # for python 3.8


def get_str_list_from_dict(data: dict, key: str) -> list[str]:
    content = None
    try:
        content = data[key]
        if type(content) == type(str()):  # noqa: E721
            content = [content]
    except KeyError:
        content = None
    finally:
        return content


def get_str_from_dict(data: dict, key: str) -> str:
    content = None
    try:
        content = data[key]
    except KeyError:
        content = None
    finally:
        return content


def get_bool_from_dict(data: dict, key: str) -> bool:
    content = None
    try:
        content = data[key]
    except KeyError:
        content = None
    finally:
        if content is not None:
            content = content and True

        return content

