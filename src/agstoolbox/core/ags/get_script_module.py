from __future__ import annotations  # for python 3.8

import os.path

import defusedxml.ElementTree as ETree
from xml.etree.ElementTree import Element

from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.script_module import ScriptModule


def _module_element_from_project(game_project: GameProject, module_name: str) -> Element | None:
    tree = ETree.parse(game_project.path)
    root = tree.getroot()
    scripts_and_header_htags = root.findall('.//ScriptAndHeader')
    script_htag: Element | None = None
    for sah_htag in scripts_and_header_htags:
        sah_script_htag = sah_htag.find('ScriptAndHeader_Script')
        script_htag = sah_script_htag.find('Script')
        script_name_htag = script_htag.find('Name')
        if script_name_htag.text == module_name:
            break
        script_fname_htag = script_htag.find('FileName')
        if script_fname_htag.text[:-4] == module_name:
            break
        script_htag = None

    if script_htag is None:
        return None
    return script_htag


def exists_module_in_game_project(game_project: GameProject, module_name: str) -> bool:
    script_htag = _module_element_from_project(game_project, module_name)
    return (script_htag is not None) and True


def module_from_game_project(game_project: GameProject, module_name: str) -> ScriptModule | None:
    script_htag = _module_element_from_project(game_project, module_name)

    if script_htag is None:
        return None

    script_filename_htag = script_htag.find('FileName')
    module_filename = script_filename_htag.text[:-4]
    header_filename = module_filename + ".ash"
    script_filename = module_filename + ".asc"
    full_header_filename = os.path.abspath(os.path.join(game_project.directory, header_filename))
    full_script_filename = os.path.abspath(os.path.join(game_project.directory, script_filename))

    sm: ScriptModule = ScriptModule()
    sm.basename = module_filename
    sm.name = script_htag.find('Name').text
    sm.version = script_htag.find('Version').text
    sm.author = script_htag.find('Author').text
    sm.unique_key = script_htag.find('Key').text
    sm.description = script_htag.find('Description').text

    sm.unique_key_int = int(sm.unique_key)

    with open(full_header_filename, "r") as f:
        sm.header = f.read()

    with open(full_script_filename, "r") as f:
        sm.script = f.read()

    return sm
