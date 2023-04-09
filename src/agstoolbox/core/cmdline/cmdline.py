from __future__ import annotations  # for python 3.8

from operator import attrgetter
from pathlib import Path
from sys import exit
import argparse
import shtab  # for completion magic


from agstoolbox import __title__, __version__, __copyright__, __license__
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.ags_local_run import ags_editor_load_project, start_ags_editor
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.get_game_projects import list_game_projects_in_dir, \
    list_game_projects_in_dir_list, valid_gameagf_file_to_game_project
from agstoolbox.core.ags.get_local_ags_editors import list_probable_ags_editors_in_dir, \
    list_ags_editors_in_dir_list
from agstoolbox.core.cmdline.cmdline_download import cmdline_download_release_to_cache
from agstoolbox.core.gh.install_release import is_install_dir_busy, install_release_from_cache
from agstoolbox.core.gh.list_releases import list_releases, get_latest_release_family, \
    get_release_version
from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings.settings import Settings
from agstoolbox.core.version.version import Version
from agstoolbox.core.version.version_utils import version_str_to_version


def get_unique_game_project_in_path(project_path: str) -> GameProject | None:
    game_project: GameProject | None = valid_gameagf_file_to_game_project(project_path)

    if game_project is None:
        projects: list[GameProject] = list_game_projects_in_dir(project_path)
        if len(projects) != 1:
            print('WARN: Invalid project path, not exactly 1 game project found!')
            return None

        game_project = projects[0]

    return game_project


def at_cmd_list_projects(args):
    a_path: str | None = args.path

    if a_path is None:
        Settings().load()
        prj_dirs: list[str] = Settings().get_project_search_dirs()
        projects = list_game_projects_in_dir_list(prj_dirs)

    else:
        projects = list_game_projects_in_dir(a_path)

    for p in projects:
        print(p.name + ', ' + p.ags_editor_version.as_str + ', ' + p.path)
    pass


def at_cmd_list_editors(args):
    is_unmanaged: bool = args.unmanaged and True
    is_download: bool = args.download and True
    a_path: str | None = args.path

    releases: list[Release] = []
    editors: list[LocalAgsEditor] = []
    if a_path is None:
        Settings().load()
        if is_unmanaged:
            unmanaged_dirs: list[str] = Settings().get_manually_installed_editors_search_dirs()
            editors = list_ags_editors_in_dir_list(unmanaged_dirs)
        elif is_download:
            releases = list_releases()
        else:
            managed_dir: str = Settings().get_tools_install_dir()
            editors = list_probable_ags_editors_in_dir(managed_dir)

    else:
        editors = list_probable_ags_editors_in_dir(a_path)

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
    force: bool = True and args.force
    install_arg: str = args.VERSION_OR_PROJECT_PATH

    if install_arg is None or install_arg == "":
        print('ERROR: Editor Version specified is invalid!')
        return

    editor_version: Version | None = None
    if Path(install_arg).exists():
        game_project: GameProject | None = get_unique_game_project_in_path(install_arg)
        if game_project is not None:
            editor_version = game_project.ags_editor_version

    release_to_install: Release = Release()
    releases: list[Release] = list_releases()

    if editor_version is None or editor_version.as_int < 3000000000:
        # arg was really a version
        editor_version = version_str_to_version(install_arg)
        if editor_version.improv == "0" and editor_version.patch == "0":
            release_to_install = get_latest_release_family(releases, editor_version.family)

    with release_to_install as ri:
        if ri is None or ri.archive_url is None or len(ri.archive_url) <= 1:
            release_to_install = get_release_version(releases, editor_version)

    if release_to_install is None:
        print('ERROR: Editor Version specified is invalid!')
        return

    if is_install_dir_busy(release_to_install) and not force:
        print('ERROR: Editor Version already installed!')
        return

    print("Will install managed AGS Editor release " + release_to_install.version.as_str)

    cmdline_download_release_to_cache(release_to_install)

    print("Extracting...")
    install_release_from_cache(release_to_install)
    print("Installed release " + release_to_install.version.as_str)
    pass


def at_cmd_open_editor(args):
    editor_version: Version = version_str_to_version(args.EDITOR_VERSION)

    if editor_version is None or editor_version.as_int < 3000000000:
        print('ERROR: Invalid version!')
        return

    managed_dir: str = Settings().get_tools_install_dir()
    editors = list_probable_ags_editors_in_dir(managed_dir)

    for editor in editors:
        if editor.version.as_int == editor_version.as_int:
            start_ags_editor(editor)
            return

    unmanaged_dirs: list[str] = Settings().get_manually_installed_editors_search_dirs()
    un_editors = list_ags_editors_in_dir_list(unmanaged_dirs)

    for editor in un_editors:
        if editor.version.as_int == editor_version.as_int:
            start_ags_editor(editor)
            return

    print("WARN: Failed to find exact match of AGS Editor, will try to find a compatible one")

    filtered_editors = [ae for ae in editors if ae.version.family == editor_version.family]
    filtered_editors.sort(key=attrgetter("version.as_int"), reverse=True)
    if len(filtered_editors) >= 1:
        start_ags_editor(filtered_editors[0])
        return

    filtered_un_editors = [ae for ae in un_editors if ae.version.family == editor_version.family]
    filtered_un_editors.sort(key=attrgetter("version.as_int"), reverse=True)
    if len(filtered_un_editors) >= 1:
        start_ags_editor(filtered_un_editors[0])
        return

    print("ERROR: No compatible AGS Editor available")


def at_cmd_open_project(args):
    prj_path: str = args.PROJECT_PATH

    if not Path(prj_path).exists():
        print('ERROR: Invalid project path')
        return

    game_project: GameProject | None = get_unique_game_project_in_path(prj_path)
    if game_project is None:
        print('ERROR: Invalid project path')
        return

    project_version: Version = game_project.ags_editor_version

    managed_dir: str = Settings().get_tools_install_dir()
    editors = list_probable_ags_editors_in_dir(managed_dir)

    for editor in editors:
        if editor.version.as_int == project_version.as_int:
            ags_editor_load_project(editor, game_project)
            return

    unmanaged_dirs: list[str] = Settings().get_manually_installed_editors_search_dirs()
    editors = list_ags_editors_in_dir_list(unmanaged_dirs)

    for editor in editors:
        if editor.version.as_int == project_version.as_int:
            ags_editor_load_project(editor, game_project)
            return

    print("ERROR: Failed to find exact match of AGS Editor")


def at_cmd_open(args):
    is_editor_open: bool = args.sub_open == 'editor'
    is_proj_open: bool = args.sub_open == 'project'

    if is_proj_open:
        at_cmd_open_project(args)
    elif is_editor_open:
        at_cmd_open_editor(args)
    else:
        print('ERROR: Invalid open command!')


def at_cmd_settings_show(args):
    show_what: str | None = args.sub_setting_param

    if show_what is None or show_what == 'all':
        print(Settings().dump())
    elif show_what == 'project_search_dirs':
        print("Project Search Dirs:", ', '.join(Settings().get_project_search_dirs()))
    elif show_what == 'tools_install_dir':
        print("Tools Install Dir:", Settings().get_tools_install_dir())
    else:
        print('ERROR: Invalid settings show command!')
        return


def at_cmd_settings_set(args):
    set_what: str | None = args.sub_setting_param

    if set_what == 'tools_install_dir':
        Settings().set_tools_install_dir(args.value)
    else:
        print('ERROR: Invalid settings set command!')
        return

    Settings().save()


def at_cmd_settings(args):
    is_show_settings: bool = args.sub_settings == 'show'
    is_set_settings: bool = args.sub_settings == 'set'

    if is_show_settings:
        at_cmd_settings_show(args)
        return
    elif is_set_settings:
        at_cmd_settings_set(args)
        return
    else:
        print('ERROR: Invalid settings command!')
        return


def cmdline(show_help_when_empty: bool, program_name: str):
    parser = argparse.ArgumentParser(
        prog=program_name,
        description=__title__ + ' is an application to help manage AGS Editor versions.',
        epilog=__copyright__ + ", " + __license__ + ".")

    shtab.add_argument_to(parser, ["-s"])  # magic!
    parser.add_argument(
        '-v', '--version', action='store_true', default=False, help='get software version.')
    subparsers = parser.add_subparsers(help='command')

    # create the parser for the "command_a" command
    p_l = subparsers.add_parser('list', help='lists things')
    p_l.set_defaults(func=at_cmd_list)
    p_ll = p_l.add_subparsers(title='sub_list', dest='sub_list')
    p_lle = p_ll.add_parser('editors', help='lists AGS Editors, by default only managed editors')
    p_lle.add_argument('-p', '--path', action='store', default=None, type=str,
                       help='look for AGS Editors in specific path, ignore settings'
                       ).complete = shtab.DIRECTORY
    p_lle.add_argument(
        '-u', '--unmanaged', action='store_true', default=False,
        help='search for unmanaged editors in settings')
    p_lle.add_argument(
        '-d', '--download', action='store_true', default=False,
        help='lists for editors available for download')
    p_llp = p_ll.add_parser('projects', help='lists AGS Projects')
    p_llp.add_argument('-p', '--path', action='store', default=None, type=str,
                       help='the path to look for list').complete = shtab.DIRECTORY

    p_i = subparsers.add_parser('install', help='install tools')
    p_i.set_defaults(func=at_cmd_install)
    p_ii = p_i.add_subparsers(title='sub_install', dest='sub_install')
    p_iie = p_ii.add_parser('editor', help='install managed AGS Editor')
    p_iie.add_argument('VERSION_OR_PROJECT_PATH',
                       help='version to install or project to grab editor version')
    p_iie.add_argument('-f', '--force', action='store_true', default=None,
                       help='forces installation, overwrite if already exists')

    p_o = subparsers.add_parser('open', help='open an editor or project')
    p_o.set_defaults(func=at_cmd_open)
    p_oo = p_o.add_subparsers(title='sub_open', dest='sub_open')
    p_ooe = p_oo.add_parser('editor', help='open AGS Editor, by default only managed editors')
    p_ooe.add_argument('EDITOR_VERSION',
                       help='Editor version to open')
    p_oop = p_oo.add_parser('project', help='open AGS Project')
    p_oop.add_argument('PROJECT_PATH',
                       help='path to the project to be opened').complete = shtab.FILE

    # settings command
    p_s = subparsers.add_parser('settings', help='modify or show settings')
    p_s.set_defaults(func=at_cmd_settings)
    p_ss = p_s.add_subparsers(title='sub_settings', dest='sub_settings')

    p_sss = p_ss.add_parser('show', help='show settings values')
    p_sssp = p_sss.add_subparsers(title='sub_setting_param',
                                  dest='sub_setting_param', required=False)
    p_sssp_proj = p_sssp.add_parser('project_search_dirs', help='show project search dirs')
    p_sssp_tools = p_sssp.add_parser('tools_install_dir', help='show tools install dir')

    p_sss = p_ss.add_parser('set', help='set settings values')
    p_sssp = p_sss.add_subparsers(title='sub_setting_param', dest='sub_setting_param')
    p_sssp_tools = p_sssp.add_parser('tools_install_dir', help='set tools install dir')
    p_sssp_tools.add_argument('value',
                              help='path to the tools install dir').complete = shtab.DIRECTORY

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
