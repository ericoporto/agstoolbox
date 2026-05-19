#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""update_version.py — set the project version in one command.

Usage:
    python helper_scripts/update_version.py 1.2.3
"""
import os
import re
import sys
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root_dir = Path(Path(current_dir).parent)


def version_to_triplet_part(version: str) -> tuple[int, int, int]:
    parts = version.strip().split('.')
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        sys.exit(f"error: version must be x.y.z (got {version!r})")
    return int(parts[0]), int(parts[1]), int(parts[2])


def update_init(version: str) -> None:
    filepath = "src/agstoolbox/__init__.py"
    path = Path(os.path.join(project_root_dir, filepath))
    text = ""
    with open(path, "r", encoding="utf-8", newline='') as f:
        text = f.read()
    text = re.sub(r"(__version__\s*=\s*')[^']*(')", rf"\g<1>{version}\2", text)
    with open(path, "w", encoding="utf-8", newline='') as f:
        f.write(text)

    print(f"  {filepath}  set version to: '{version}'")


def update_version_info(file_name: str, version: str, x: int, y: int, z: int) -> None:
    path = Path(os.path.join(project_root_dir, file_name))
    text = ""
    with open(path, "r", encoding="utf-8", newline='') as f:
        text = f.read()

    tuple_str = f'({x}, {y}, {z}, 0)'
    text = re.sub(r'filevers\s*=\s*\([^)]*\)', f'filevers={tuple_str}', text)
    text = re.sub(r'prodvers\s*=\s*\([^)]*\)', f'prodvers={tuple_str}', text)

    quad = f'{version}.0'
    text = re.sub(r"(StringStruct\('FileVersion',\s*')[^']*(')", rf"\g<1>{quad}\2", text)
    text = re.sub(r"(StringStruct\('ProductVersion',\s*')[^']*(')", rf"\g<1>{quad}\2", text)


    with open(path, "w", encoding="utf-8", newline='') as f:
        f.write(text)
    print(f"  {file_name}  set version to: '{version}' and '{quad}'")


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(f"usage: python {sys.argv[0]} x.y.z")
    version = sys.argv[1]
    x, y, z = version_to_triplet_part(version)
    print(f"Setting version to {version}")
    update_init(version)
    update_version_info("agstoolbox_version_info.txt", version, x, y, z)
    update_version_info("atbx_version_info.txt", version, x, y, z)
    print("Done.\n")


if __name__ == '__main__':
    main()
