from __future__ import annotations  # for python 3.8
import pefile


class ExeFileDescriptor:
    product_name = None
    original_filename = None
    internal_name = None
    file_version = None
    product_version = None
    company_name = None


def is_valid_exe(filepath: str) -> bool:
    is_exe = False
    try:
        pe = pefile.PE(filepath)
        is_exe = pe.is_exe()
    except pefile.PEFormatError:
        return False
    finally:
        return is_exe


def get_exe_information(filepath: str) -> ExeFileDescriptor:
    string_info = {}
    pe = None
    try:
        pe = pefile.PE(filepath)
    except pefile.PEFormatError:
        return ExeFileDescriptor()

    if not pe.is_exe():
        return ExeFileDescriptor()

    for fileinfo in pe.FileInfo[0]:
        if fileinfo.Key.decode() == 'StringFileInfo':
            for st in fileinfo.StringTable:
                for entry in st.entries.items():
                    string_info[entry[0].decode()] = entry[1].decode()

    bin_exe = ExeFileDescriptor()
    bin_exe.product_name = string_info['ProductName']  # should be 'Adventure Game Studio'
    bin_exe.original_filename = string_info['OriginalFilename']  # should be 'AGSEditor.exe'
    bin_exe.product_version = string_info['ProductVersion']  # should be something like '3.5.1.14'
    bin_exe.file_version = string_info['FileVersion']  # should be something like '3.5.1.14'
    bin_exe.internal_name = string_info['InternalName']  # should be 'AGSEditor.exe'
    bin_exe.company_name = string_info['CompanyName']  # should be 'AGS'

    return bin_exe
