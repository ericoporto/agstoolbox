from __future__ import annotations  # for python 3.8

from operator import attrgetter
from pathlib import Path
from sys import exit
import argparse
from typing import Callable

import shtab  # for completion magic

from agstoolbox import __title__, __version__, __copyright__, __license__
from agstoolbox.core.ags.ags_editor import LocalAgsEditor
from agstoolbox.core.ags.ags_export import export_script_module_from_project
from agstoolbox.core.ags.ags_local_run import ags_editor_load, ags_editor_start, \
    ags_editor_build, ags_editor_template_build
from agstoolbox.core.ags.ags_template import create_template_from_project, \
    editor_supports_template_export, fix_editor_built_template
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.get_game_projects import list_game_projects_in_dir, \
    list_game_projects_in_dir_list, get_unique_game_project_in_path
from agstoolbox.core.ags.get_local_ags_editors import list_probable_ags_editors_in_dir, \
    list_ags_editors_in_dir_list
from agstoolbox.core.ags.get_script_module import exists_module_in_game_project
from agstoolbox.core.ags.package_compiled import package_compiled_game
from agstoolbox.core.cmdline.cmdline_download import cmdline_download_release_to_cache
from agstoolbox.core.gh.agstoolbox_update import is_latest_agstoolbox_release
from agstoolbox.core.gh.install_release import is_install_dir_busy, install_release_from_cache
from agstoolbox.core.gh.list_releases import list_releases, get_latest_release_family, \
    get_release_version
from agstoolbox.core.gh.release import Release
from agstoolbox.core.settings.settings import Settings
from agstoolbox.core.version.version import Version
from agstoolbox.core.version.version_utils import version_str_to_version


class MetaCmdProjectArgs:
    which_only: bool
    block: bool
    prj_path: str
    timeout: int
    editor_version: Version | None


def meta_cmd_project(args, is_open: bool,
                     ags_editor_proj_command: Callable[
                         [LocalAgsEditor, GameProject, bool, int], int] = None) -> int:
    which_only: bool = False
    if is_open:
        which_only = args.which_editor and True
    block: bool = not getattr(args, "non_blocking", False)
    prj_path: str = args.PROJECT_PATH
    timeout: int = getattr(args, "timeout", 0)
    editor_version: str | None = getattr(args, "editor", None)

    meta_args: MetaCmdProjectArgs = MetaCmdProjectArgs()
    meta_args.block = block
    meta_args.which_only = which_only
    meta_args.prj_path = prj_path
    meta_args.timeout = timeout
    meta_args.editor_version = None if (editor_version is None) or (len(str(editor_version)) < 1) \
        else version_str_to_version(editor_version)
    return base_meta_cmd_project(meta_args, ags_editor_proj_command)

def base_meta_cmd_project(meta_args: MetaCmdProjectArgs,
                     ags_editor_proj_command: Callable[
                         [LocalAgsEditor, GameProject, bool, int], int] = None) -> int:
    which_only: bool = meta_args.which_only
    block: bool = meta_args.block
    prj_path: str = meta_args.prj_path
    timeout: int = meta_args.timeout
    editor_version: Version | None = meta_args.editor_version

    if not Path(prj_path).exists():
        print('ERROR: Invalid project path')
        return -1

    game_project: GameProject | None = get_unique_game_project_in_path(prj_path)
    if game_project is None:
        print('ERROR: Invalid project path')
        return -1

    project_version: Version = game_project.ags_editor_version

    if editor_version is None:
        editor_version = project_version

    managed_dir: str = Settings().get_tools_install_dir()
    editors = list_probable_ags_editors_in_dir(managed_dir)

    editor_candidate: LocalAgsEditor | None = None

    for editor in editors:
        if editor.version.as_int == editor_version.as_int:
            editor_candidate = editor
            break

    if editor_candidate is None:
        unmanaged_dirs: list[str] = Settings().get_manually_installed_editors_search_dirs()
        editors = list_ags_editors_in_dir_list(unmanaged_dirs)

        for editor in editors:
            if editor.version.as_int == editor_version.as_int:
                editor_candidate = editor
                break

    if editor_candidate is None:
        print("ERROR: Failed to find exact match of AGS Editor, wanted " + editor_version.as_str)
        return -1

    if which_only:
        print(editor_candidate.path)
        return 0

    return ags_editor_proj_command(editor_candidate, game_project, block, timeout)


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
    quiet: bool = True and args.quiet
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

    ri = release_to_install
    if ri is None or ri.archive_url is None or len(ri.archive_url) <= 1:
        release_to_install = get_release_version(releases, editor_version)

    if release_to_install is None:
        print('ERROR: Editor Version specified is invalid!')
        return

    if is_install_dir_busy(release_to_install) and not force:
        print('ERROR: Editor Version already installed!')
        return

    print("Will install managed AGS Editor release " + release_to_install.version.as_str)

    cmdline_download_release_to_cache(release_to_install, quiet)

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
            ags_editor_start(editor)
            return

    unmanaged_dirs: list[str] = Settings().get_manually_installed_editors_search_dirs()
    un_editors = list_ags_editors_in_dir_list(unmanaged_dirs)

    for editor in un_editors:
        if editor.version.as_int == editor_version.as_int:
            ags_editor_start(editor)
            return

    print("WARN: Failed to find exact match of AGS Editor( " + editor_version.as_str +
          " ), will try to find a compatible one")

    filtered_editors = [ae for ae in editors if ae.version.family == editor_version.family]
    filtered_editors.sort(key=attrgetter("version.as_int"), reverse=True)
    if len(filtered_editors) >= 1:
        ags_editor_start(filtered_editors[0])
        return

    filtered_un_editors = [ae for ae in un_editors if ae.version.family == editor_version.family]
    filtered_un_editors.sort(key=attrgetter("version.as_int"), reverse=True)
    if len(filtered_un_editors) >= 1:
        ags_editor_start(filtered_un_editors[0])
        return

    print("ERROR: No compatible AGS Editor available, wanted " + editor_version.family)


def at_cmd_open_project(args):
    meta_cmd_project(args, True, ags_editor_load)
    return


def at_cmd_open(args):
    is_editor_open: bool = args.sub_open == 'editor'
    is_proj_open: bool = args.sub_open == 'project'

    if is_proj_open:
        at_cmd_open_project(args)
    elif is_editor_open:
        at_cmd_open_editor(args)
    else:
        print('ERROR: Invalid open command!')


def at_cmd_build(args):
    exit_code: int = meta_cmd_project(args, False, ags_editor_build)
    if exit_code != 0:
        exit(exit_code)
    return


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


def at_cmd_export_template_editor(
        game_project: GameProject, out_dir: str, template_name: str, timeout: int = 0) -> int:
    meta_args: MetaCmdProjectArgs = MetaCmdProjectArgs()
    meta_args.block = True
    meta_args.which_only = False
    meta_args.prj_path = game_project.path
    meta_args.timeout = timeout
    meta_args.editor_version = None

    if not editor_supports_template_export(game_project):
        print('ERROR: Project uses Editor "' + game_project.ags_editor_version.as_str +
              '", which doesn\'t support /maketemplate command')
        return -1

    res: int = base_meta_cmd_project(meta_args, ags_editor_template_build)
    success: bool = fix_editor_built_template(game_project, out_dir, template_name)
    if not success:
        print('ERROR: Failed to rename template')
        return -1

    return res


def at_cmd_export(args):
    target_name: str = str()
    prj_path: str = args.PROJECT_PATH
    out_dir: str = args.OUT_DIR
    force_editor: bool = args.force_editor
    timeout: int = args.timeout
    if args.sub_export == 'script':
        target_name = args.MODULE_NAME
    else:
        target_name = args.TEMPLATE_NAME

    if not Path(prj_path).exists():
        print('ERROR: Invalid project path')
        return -1

    game_project: GameProject | None = get_unique_game_project_in_path(prj_path)
    if game_project is None:
        print('ERROR: Invalid project path')
        return -1

    if out_dir is None:
        out_dir = game_project.directory

    if not Path(out_dir).exists():
        print('ERROR: Invalid output dir path')
        return -1

    if args.sub_export == 'script':
        mod_name: str = target_name
        if not exists_module_in_game_project(game_project, mod_name):
            print('ERROR: Module "' + mod_name + '" doesn\'t exist in Game Project')
            return -1

        try:
            export_script_module_from_project(game_project, mod_name, out_dir)
        except:
            return -1
        return 0
    else:
        if force_editor:
            return at_cmd_export_template_editor(game_project=game_project,
                                          template_name=target_name,
                                          out_dir=out_dir,
                                          timeout=timeout)
        else:
            try:
                create_template_from_project(game_project, target_name, out_dir)
            except:
                return -1
            return 0


def at_cmd_pack(args):
    prj_path: str = args.PROJECT_PATH

    if not Path(prj_path).exists():
        print('ERROR: Invalid project path')
        return -1

    game_project: GameProject | None = get_unique_game_project_in_path(prj_path)
    if game_project is None:
        print('ERROR: Invalid project path')
        return -1

    package_compiled_game(game_project)

    return 0

def cmdline(show_help_when_empty: bool, program_name: str):
    parser = argparse.ArgumentParser(
        prog=program_name,
        description=__title__ + ' is an application to help manage AGS Editor versions.',
        epilog=__copyright__ + ", " + __license__ + ".")

    shtab.add_argument_to(parser, ["-s"])  # magic!
    parser.add_argument(
        '-v', '--version', action='store_true', default=False,
        help='get software version.')
    subparsers = parser.add_subparsers(help='command')

    # list command
    p_l = subparsers.add_parser('list', help='lists things')
    p_l.set_defaults(func=at_cmd_list)
    p_ll = p_l.add_subparsers(title='sub_list', dest='sub_list')
    p_lle = p_ll.add_parser('editors',
                            help='lists AGS Editors, by default only managed editors')
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

    # install command
    p_i = subparsers.add_parser('install', help='install tools')
    p_i.set_defaults(func=at_cmd_install)
    p_ii = p_i.add_subparsers(title='sub_install', dest='sub_install')
    p_iie = p_ii.add_parser('editor', help='install managed AGS Editor')
    p_iie.add_argument('VERSION_OR_PROJECT_PATH',
                       help='version to install or project to grab editor version')
    p_iie.add_argument('-f', '--force', action='store_true', default=False,
                       help='forces installation, overwrite if already exists')
    p_iie.add_argument('-q', '--quiet', action='store_true', default=False,
                       help='do not print download progress')

    # open command
    p_o = subparsers.add_parser('open', help='open an editor or project')
    p_o.set_defaults(func=at_cmd_open)
    p_oo = p_o.add_subparsers(title='sub_open', dest='sub_open')
    p_ooe = p_oo.add_parser('editor', help='open AGS Editor, by default only managed editors')
    p_ooe.add_argument('EDITOR_VERSION',
                       help='Editor version to open')
    p_oop = p_oo.add_parser('project', help='open AGS Project')
    p_oop.add_argument('PROJECT_PATH',
                       help='path to the project to be opened').complete = shtab.FILE
    p_oop.add_argument('-n', '--non-blocking', action='store_true', default=False,
                       help='don\'t wait for Editor to close to continue')
    p_oop.add_argument('-w', '--which-editor', action='store_true', default=False,
                       help='give editor path only, don\'t open project')
    p_oop.add_argument('-e', '--editor', metavar='VER', type=str, default=None,
                     help='version of editor to open')

    # build command
    p_b = subparsers.add_parser('build', help='builds an ags project')
    p_b.set_defaults(func=at_cmd_build)
    p_b.add_argument('PROJECT_PATH',
                     help='path to the project to be built').complete = shtab.FILE
    p_b.add_argument('-n', '--non-blocking', action='store_true', default=False,
                     help='don\'t wait for Editor to close to continue')
    p_b.add_argument('-t', '--timeout', metavar='SEC', type=int, default=0,
                     help='seconds to wait before interrupting the build')
    p_b.add_argument('-e', '--editor', metavar='VER', type=str, default=None,
                     help='version of editor to open')

    # settings command
    p_s = subparsers.add_parser('settings', help='modify or show settings')
    p_s.set_defaults(func=at_cmd_settings)
    p_ss = p_s.add_subparsers(title='sub_settings', dest='sub_settings')

    p_ssh = p_ss.add_parser('show', help='show settings values')
    p_sshp = p_ssh.add_subparsers(title='sub_setting_param',
                                  dest='sub_setting_param', required=False)
    p_sshp.add_parser('project_search_dirs', help='show project search dirs')
    p_sshp.add_parser('tools_install_dir', help='show tools install dir')

    p_sse = p_ss.add_parser('set', help='set settings values')
    p_ssep = p_sse.add_subparsers(title='sub_setting_param', dest='sub_setting_param')
    p_ssep_t = p_ssep.add_parser('tools_install_dir', help='set tools install dir')
    p_ssep_t.add_argument('value',
                          help='path to the tools install dir').complete = shtab.DIRECTORY

    # export command
    p_e = subparsers.add_parser('export', help='export from ags project')
    p_e.set_defaults(func=at_cmd_export)
    p_ee = p_e.add_subparsers(title='sub_export', dest='sub_export')
    p_ees = p_ee.add_parser('script', help='export script module from project')
    p_ees.add_argument('PROJECT_PATH',
                       help='path to the project with the module').complete = shtab.FILE
    p_ees.add_argument('MODULE_NAME',
                       help='name of the script module')
    p_ees.add_argument('OUT_DIR',
                       help='where to export the script module').complete = shtab.DIRECTORY

    p_eet = p_ee.add_parser('template', help='export project as template')
    p_eet.add_argument('PROJECT_PATH',
                       help='path to the project to be exported').complete = shtab.FILE
    p_eet.add_argument('TEMPLATE_NAME',
                       help='name of the template (e.g. "template.agt")')
    p_eet.add_argument('OUT_DIR',
                       help='where to export the template').complete = shtab.DIRECTORY
    p_eet.add_argument('-f', '--force-editor', action='store_true', default=False,
                     help='use editor for template export')
    p_eet.add_argument('-t', '--timeout', metavar='SEC', type=int, default=0,
                     help='seconds to wait before interrupting editor export')

    # pack
    p_p = subparsers.add_parser('pack', help='package build results')
    p_p.set_defaults(func=at_cmd_pack)
    p_p.add_argument('PROJECT_PATH',
                       help='path to the project built to archive').complete = shtab.FILE

    args = parser.parse_args()
    if 'func' in args.__dict__:
        args.func(args)

    if args.version:
        print(__title__ + "  v " + __version__)
        if not is_latest_agstoolbox_release():
            print('There is a new release of AGSToolbox.')
        exit()

    if any(vars(args).values()):
        exit()

    if show_help_when_empty:
        parser.print_usage()

    return []
