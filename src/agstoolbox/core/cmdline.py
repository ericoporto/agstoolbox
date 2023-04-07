from __future__ import annotations  # for python 3.8
from sys import exit
import argparse

from agstoolbox import __title__, __version__, __copyright__, __license__
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.get_game_projects import list_game_projects_in_dir, \
    list_game_projects_in_dir_list
from agstoolbox.core.ags.get_local_ags_editors import list_probable_ags_editors_in_dir, \
    list_ags_editors_in_dir_list
from agstoolbox.core.gh.list_releases import list_releases
from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings.settings import Settings


def at_cmd_list_projects(args):
    if args.path is None:
        Settings().load()
        prj_dirs: list[str] = Settings().get_project_search_dirs()
        projects = list_game_projects_in_dir_list(prj_dirs)

    else:
        projects = list_game_projects_in_dir(args.path)

    for p in projects:
        print(p.name + ', ' + p.ags_editor_version.as_str + ', ' + p.path)
    pass


def at_cmd_list_editors(args):
    releases: list[Release] = []
    editors: list[LocalAgsEditor] = []
    if args.path is None:
        Settings().load()
        if args.unmanaged:
            unmanaged_dirs: list[str] = Settings().get_manually_installed_editors_search_dirs()
            editors = list_ags_editors_in_dir_list(unmanaged_dirs)
        elif args.download:
            releases = list_releases()
        else:
            managed_dir: str = Settings().get_tools_install_dir()
            editors = list_probable_ags_editors_in_dir(managed_dir)

    else:
        editors = list_probable_ags_editors_in_dir(args.path)

    for e in editors:
        print(e.name + ', ' + e.version.as_str + ', ' + e.path)
    pass

    for r in releases:
        print('download' + ', ', r.version.as_str + ', ' + r.html_url)
    pass


def at_cmd_list(args):
    is_editor_list: bool = args.sub_list == 'editors'
    is_proj_list: bool = args.sub_list == 'projects'

    if is_proj_list:
        at_cmd_list_projects(args)
    elif is_editor_list:
        at_cmd_list_editors(args)
    else:
        print('ERROR: Invalid list command!')


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
    p_l = subparsers.add_parser('list', help='lists things')
    p_l.set_defaults(func=at_cmd_list)
    p_ll = p_l.add_subparsers(title='sub_list', dest='sub_list')
    p_lle = p_ll.add_parser('editors', help='lists AGS Editors, by default only managed editors')
    p_lle.add_argument('-p', '--path', action='store', default=None, type=str,
                       help='look for AGS Editors in specific path, ignore settings')
    p_lle.add_argument(
        '-u', '--unmanaged', action='store_true', default=False,
        help='search for unmanaged editors in settings')
    p_lle.add_argument(
        '-d', '--download', action='store_true', default=False,
        help='lists for editors available for download')
    p_llp = p_ll.add_parser('projects', help='lists AGS Projects')
    p_llp.add_argument('-p', '--path', action='store', default=None, type=str,
                       help='the path to look for list')

    p_i = subparsers.add_parser('install', help='install thing help')
    p_i.set_defaults(func=at_cmd_install)

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
