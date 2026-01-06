from __future__ import annotations  # for python 3.8

import subprocess
import sys

def unix_path_to_wine_path(path: str) -> str | None:
    command = ['winepath', '-w', path]
    try:
        result = subprocess.run(command,
                                check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True,
                                encoding='utf-8'
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print('ERROR: failed to convert path, ' + e.stderr)
        return None
    except FileNotFoundError:
        print('ERROR: winepath command not found. Ensure Wine is installed and in your PATH.')
        return None
