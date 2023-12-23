from __future__ import annotations  # for python 3.8

import os.path
from struct import pack
from typing import BinaryIO

from agstoolbox.core.ags.script_module import (ScriptModule, MODULE_FILE_SIGNATURE,
                                               MODULE_FILE_SECTION, MODULE_FILE_TRAILER)
from agstoolbox.core.ags.game_project import GameProject
from agstoolbox.core.ags.get_script_module import module_from_game_project


def export_script_module_from_project(game_project: GameProject, module_name: str, out: str | None):
    if out is None:
        out = game_project.directory

    sm: ScriptModule = module_from_game_project(game_project, module_name)
    export_script_module(sm, out, game_project.encoding, game_project.codepage)


def export_script_module(sm: ScriptModule, out_dir: str, enc: str, codepage: int):
    module_filename = os.path.join(out_dir, sm.basename + ".scm")

    with open(module_filename, 'wb') as f:
        f.write(MODULE_FILE_SIGNATURE)
        f.write(pack('i', 1))  # version

        write_string_terminated(sm.author, enc, f)
        write_string_terminated(sm.description, enc, f)
        write_string_terminated(sm.name, enc, f)
        write_string_terminated(sm.version, enc, f)

        write_string_long_terminated(sm.script, enc, f)
        write_string_long_terminated(sm.header, enc, f)

        f.write(pack('i', sm.unique_key_int))
        f.write(pack('i', 0))  # Permissions (obsolete)
        f.write(pack('i', 0))  # We are owner (obsolete)

        # format extension 1
        f.write(pack('I', MODULE_FILE_SECTION))
        f.write(pack('I', codepage))

        # end of format
        f.write(pack('I', MODULE_FILE_TRAILER))


def write_string_terminated(text: str, enc: str, f: BinaryIO):
    text_bytes: bytes = text.encode(encoding=enc)
    f.write(text_bytes)
    f.write(b'\x00')


def write_string_long_terminated(text: str, enc: str, f: BinaryIO):
    text_bytes: bytes = text.encode(encoding=enc)
    f.write(pack('I', len(text_bytes)))
    f.write(text_bytes)
    f.write(b'\x00')

