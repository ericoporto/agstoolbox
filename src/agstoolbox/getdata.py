# -*- coding: utf-8 -*-
import os.path
import sys

from agstoolbox.core.utils.pyinstaller_hacks import is_running_from_pyinstaller, get_extracted_path

# am I running from pyinstaller ?
if is_running_from_pyinstaller():
    # yes, running from pyinstaller
    data_path = os.path.join(os.path.join(get_extracted_path()), 'data')
elif __file__:
    # no, this is the realworld
    data_path = os.path.join(os.path.dirname(__file__), 'data')


def path(filename):
    """
    Returns path for filename in data folder, like images needed for the ui.
    """
    return os.path.join(data_path, filename)
