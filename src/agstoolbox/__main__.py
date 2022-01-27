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
import argparse

from agstoolbox import __title__, __version__, __copyright__, __license__

# TODO: figure out how to avoid import when no graphical environment exists
from agstoolbox.at_trayindicator import run_tray_indicator

from agstoolbox.ags.get_game_projects import list_game_projects_in_dir


def at_cmd_list(args):
    projs = list_game_projects_in_dir(args.Path)
    for p in projs:
        print(p.name + ', ' + p.ags_editor_version + ', ' + p.path)
    pass


def at_cmd_install(args):
    print('Install: Not implemented yet!')
    print(args)
    pass


def at_cmd_run(args):
    print('Run: Not implemented yet!')
    print(args)
    pass


def main():
    """"
    agstoolbox main routine
    When you use `python -m agstoolbox`, the main routine is called.
    If you use `pip install agstoolbox`, typing agstoolbox will also call this routine.
    The objective of this function is to:
    1. load agstoolbox when called without args
    2. seeing the current version by using `--version`, and not opening agstoolbox
    """
    environ["LIBOVERLAY_SCROLLBAR"] = "0"
    parser = argparse.ArgumentParser(
        prog=__title__,
        description=__title__ + ' is an application to help manage AGS Editor versions.',
        epilog=__copyright__ + ", " + __license__ + ".")
    parser.add_argument(
        '-v', '--version', action='store_true', default=False, help='get software version.')
    subparsers = parser.add_subparsers(help='command')

    # create the parser for the "command_a" command
    parser_list = subparsers.add_parser('list', help='command_a help')
    parser_list.set_defaults(func=at_cmd_list)
    parser_list.add_argument('Path', metavar='path', type=str, help='the path to list')

    parser_install = subparsers.add_parser('install', help='install thing help')
    parser_install.set_defaults(func=at_cmd_install)

    parser_run = subparsers.add_parser('run', help='install thing help')
    parser_run.set_defaults(func=at_cmd_run)

    parser_list.add_argument('-p', '--proj', action='store_true', default=False, help='list AGS Projects')
    parser_list.add_argument('-e', '--editors', action='store_true', default=False, help='list AGS Editors')

    args = parser.parse_args()
    if 'func' in args.__dict__:
        args.func(args)

    if args.version:
        print(__title__ + "  v " + __version__)
        exit()

    if any(vars(args).values()):
        exit()

    ap_args = []
    run_tray_indicator(ap_args)


def Run():
    main()


if __name__ == "__main__":
    main()
