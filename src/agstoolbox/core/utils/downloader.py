from __future__ import annotations  # for python 3.8
from typing import Callable

import requests


def download_from_url(url: str, save_path: str, chunk_size: int = 128,
                      progress_update: Callable[[float, int, int, int], None] = None):
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get('content-length', 0))
    acc_c_size = 0
    with open(save_path, 'wb') as fd:
        for chunk in response.iter_content(chunk_size=chunk_size):
            c_size = len(chunk)*8
            acc_c_size += c_size
            completed_percent = acc_c_size / total_size_in_bytes
            if progress_update is not None:
                progress_update(completed_percent, c_size, acc_c_size, total_size_in_bytes)
            fd.write(chunk)
