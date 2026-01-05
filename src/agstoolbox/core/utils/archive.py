from __future__ import annotations  # for python 3.8

import zipfile
import tarfile
import stat
from pathlib import Path

def zip_dir(src_dir: str, out_file: str):
    src = Path(src_dir)
    out = Path(out_file)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in src.rglob('*'):
            if p.is_file():
                z.write(p, p.relative_to(src))


def tar_gz_dir(src_dir: str, out_file: str, exe_bit_files: list[str]):
    src = Path(src_dir)
    out = Path(out_file)
    with tarfile.open(out, 'w:gz') as tar:
        for p in src.rglob('*'):
            if not p.is_file():
                continue

            path_in_archive = str(p.relative_to(src).as_posix())
            print(path_in_archive)

            ti = tar.gettarinfo(p, arcname=path_in_archive)

            if path_in_archive in exe_bit_files:
                # chmod +x
                ti.mode |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH

            with p.open('rb') as f:
                tar.addfile(ti, f)

