from __future__ import annotations  # for python 3.8

import os
from typing import BinaryIO

from agstoolbox.core.ags.ags_export import write_uint8, write_string_unterminated, write_bytes, \
    write_uint, write_string_terminated, write_uint64
from agstoolbox.core.utils.file import get_relative_paths, get_size, get_file, mkdirp
from agstoolbox.core.ags.multifilelib import MultiFileLib
from agstoolbox.core.ags.multifile import MultiFile

CLIB_BEGIN_SIGNATURE = b"CLIB\x1a"
CLIB_END_SIGNATURE = b"CLIB\x01\x02\x03\x04SIGE"
CLIB_VERSION = 30  # large file support, non-encoded
MAXMULTIFILES = 256  # 1-byte index
MAX_PATH = 260  # corresponds to WinAPI definition


# Write asset library header with the table of contents.
# Currently corresponds to writing main lib file in chain in format version 30.
def write_clib_header(our_lib: MultiFileLib, f: BinaryIO):
    write_uint(0, f)  # reserved options
    write_uint(len(our_lib.data_file_names), f)  # reserved options
    for filename in our_lib.data_file_names:
        write_string_terminated(filename, 'utf-8', f)

    write_uint(len(our_lib.files), f)
    for file_info in our_lib.files:
        write_string_terminated(file_info.name, 'utf-8', f)
        write_uint8(file_info.datafile, f)
        write_uint64(file_info.offset, f)
        write_uint64(file_info.length, f)


def get_multifile_lib(files: list[str], files_base_dir: str, base_file_name: str,
                      make_file_name_assumptions: bool) -> MultiFileLib:
    our_lib: MultiFileLib = MultiFileLib()
    our_lib.files = []
    our_lib.data_file_names = []
    current_data_file = 0
    data_assets: list[str] = get_relative_paths(files, files_base_dir)
    file_count = len(files)

    for i in range(file_count):
        file = files[i]
        asset = data_assets[i]
        file_size = get_size(file)
        if len(asset) >= MAX_PATH:
            print(f"Filename too long: {asset}")
            return MultiFileLib()
        m_file: MultiFile = MultiFile()
        m_file.name = asset
        m_file.filename = file
        m_file.datafile = current_data_file
        m_file.length = file_size
        m_file.offset = 0
        our_lib.files.append(m_file)

    # First, set up ourlib.data_filenames array with all the filenames
    # so that write_clib_header will write the correct amount of data
    for i in range(current_data_file + 1):
        if make_file_name_assumptions:
            our_lib.data_file_names.append(f"{base_file_name}.{'ags' if i == 0 else i:03d}")
        else:
            our_lib.data_file_names.append(get_file(base_file_name))

    return our_lib


def find_file_in_path(file_name: str) -> str:
    paths_to_try = ["AudioCache", "Speech"]

    if os.path.exists(file_name):
        return file_name

    for path in paths_to_try:
        potential_path = os.path.join(path, file_name)
        if os.path.exists(potential_path):
            return potential_path

    return None


def make_data_file_from_multifile_lib(our_lib: MultiFileLib, out_dir: str):
    mkdirp(out_dir)

    first_data_file_full_path: str = str()
    for i, data_filename in enumerate(our_lib.data_file_names):
        output_file_name = os.path.join(out_dir, data_filename)

        if i == 0:
            first_data_file_full_path = output_file_name

        with open(output_file_name, 'ab') as wout:
            start_offset = wout.tell()
            write_bytes(CLIB_BEGIN_SIGNATURE, wout)
            write_uint8(CLIB_VERSION, wout)
            write_uint8(i, wout)
            if i == 0:
                main_header_offset = wout.tell()
                write_clib_header(our_lib, wout)

            for file_info in our_lib.files:
                if file_info.datafile == i:
                    file_info.offset = wout.tell() - start_offset
                    filename = find_file_in_path(file_info.filename)
                    if filename is None:
                        try:
                            os.remove(output_file_name)
                        except FileNotFoundError:
                            print('ERROR: Unable to find file' + file_info.filename + '.')
                            print('WARN: Do not remove files during the compilation process.')

                    with open(filename, 'rb') as infile:
                        while chunk := infile.read(1024 * 1024):
                            wout.write(chunk)
                        if infile.tell() < file_info.length:
                            raise IOError(
                                f"Error writing file '{file_info.filename}': possibly disk full")

            if start_offset > 0:
                write_uint64(start_offset, wout)
                write_bytes(CLIB_END_SIGNATURE, wout)

        with open(first_data_file_full_path, 'r+b') as wout:
            wout.seek(main_header_offset, os.SEEK_SET)
            write_clib_header(our_lib, wout)


