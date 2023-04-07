from __future__ import annotations  # for python 3.8
from sys import exit
import argparse

from agstoolbox import __title__, __version__, __copyright__, __license__
from agstoolbox.core.ags.get_game_projects import list_game_projects_in_dir


def at_cmd_list(args):
    projects = list_game_projects_in_dir(args.Path)
    for p in projects:
        print(p.name + ', ' + p.ags_editor_version.as_str + ', ' + p.path)
    pass


def at_cmd_install(args):
    print('Install: Not implemented yet!')
    print(args)
    pass


def at_cmd_run(args):
    print('Run: Not implemented yet!')
    print(args)
    pass


def cmdline(show_help_when_empty: bool):
    parser = argparse.ArgumentParser(
        prog=__title__,
        description=__title__ + ' is an application to help manage AGS Editor versions.',
        epilog=__copyright__ + ", " + __license__ + ".")
    parser.add_argument(
        '-v', '--version', action='store_true', default=False, help='get software version.')
    subparsers = parser.add_subparsers(help='command')

    # create the parser for the "command_a" command
    p_l = subparsers.add_parser('list', help='command_a help')
    p_l.set_defaults(func=at_cmd_list)
    p_l.add_argument('Path', metavar='path', type=str, help='the path to list')
    p_l.add_argument('-p', '--proj', action='store_true', default=False, help='list AGS Projects')
    p_l.add_argument('-e', '--editors', action='store_true', default=False, help='list AGS Editors')

    p_i = subparsers.add_parser('install', help='install thing help')
    p_i.set_defaults(func=at_cmd_install)

    p_r = subparsers.add_parser('run', help='install thing help')
    p_r.set_defaults(func=at_cmd_run)

    args = parser.parse_args()
    if 'func' in args.__dict__:
        args.func(args)

    if args.version:
        print(__title__ + "  v " + __version__)
        exit()

    if any(vars(args).values()):
        exit()

    if show_help_when_empty:
        parser.print_usage()

    return []
