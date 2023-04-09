#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
.. module:: agstoolbox
   :platform: Windows
   :synopsis: An application to help managing AGS Editor versions
.. moduleauthor:: Érico Vieira Porto
"""

from os import environ as environ

# TODO: figure out how to avoid import when no graphical environment exists
from agstoolbox.at_trayindicator import run_tray_indicator
from agstoolbox.core.cmdline.cmdline import cmdline
from agstoolbox import __title__


def main():
    """
    agstoolbox main routine
    When you use `python -m agstoolbox`, the main routine is called.
    If you use `pip install agstoolbox`, typing agstoolbox will also call this routine.
    The objective of this function is to:
    1. load agstoolbox when called without args
    2. seeing the current version by using `--version`, and not opening agstoolbox
    """
    environ["LIBOVERLAY_SCROLLBAR"] = "0"

    ap_args = cmdline(False, __title__)
    run_tray_indicator(ap_args)


def Run():
    main()


if __name__ == "__main__":
    main()
