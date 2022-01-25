#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
.. module:: agstoolbox
   :platform: Windows
   :synopsis: An application to help managing AGS Editor versions
.. moduleauthor:: Érico Vieira Porto
"""

from os import environ as environ
from sys import exit, argv
from PyQt6 import QtWidgets, QtCore, QtGui
import argparse

from agstoolbox import __title__, __version__, __copyright__, __license__
from agstoolbox.at_trayindicator import AtTrayIcon
from agstoolbox.at_icons import main_icon
from agstoolbox.configs import double_click_interval


def main():
    """"
    agstoolbox main routine
    When you use `python -m agstoolbox`, the main routine is called.
    If you use `pip install agstoolbox`, typing agstoolbox will also call this routine.
    The objective of this function is to:
    1. load agstoolbox when called without args
    2. seeing the current version by using `--version`, and not opening agstoolbox
    """

    global double_click_interval
    environ["LIBOVERLAY_SCROLLBAR"] = "0"
    parser = argparse.ArgumentParser(
        prog=__title__,
        description=__title__ + ' is an application to help manage AGS Editor versions.',
        epilog=__copyright__ + ", " + __license__ + ".")
    parser.add_argument(
        '-v', '--version', action='store_true', default=False, help='get software version.')

    args = parser.parse_args()

    if args.version:
        print(__title__ + "  v " + __version__)
        exit()

    ap_args = []

    app = QtWidgets.QApplication(ap_args)
    app.setQuitOnLastWindowClosed(False)
    double_click_interval = app.doubleClickInterval()

    w = QtWidgets.QWidget()
    tray_icon = AtTrayIcon(main_icon(), w)
    tray_icon.show()
    exit(app.exec())


def Run():
    main()


if __name__ == "__main__":
    main()
