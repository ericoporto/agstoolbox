import os
import hashlib


from agstoolbox.core.ags.ags_editor_validation_data import \
    AGS_EDITOR_VALIDATED_DATA_ZIP, AGS_EDITOR_VALIDATED_DATA_CONTENTS

BUF_SIZE = 131072


def validate_file(filepath, filename, validation_data):
    if filename not in validation_data:
        return False

    if not os.path.exists(filepath):
        return False

    if os.path.isdir(filepath):
        return False

    if os.path.getsize(filepath) != validation_data[filename]['size']:
        return False

    md5_checker = hashlib.md5()
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5_checker.update(data)

    return md5_checker.hexdigest() == validation_data[filename]['md5']


def validate_ags_editor_zip(z_file):
    return validate_file(z_file, os.path.basename(z_file), AGS_EDITOR_VALIDATED_DATA_ZIP)


def validate_editor_contents(filepath, filename, version):
    return validate_file(filepath, filename, AGS_EDITOR_VALIDATED_DATA_CONTENTS[version])


def validate_editor_exe(filepath, version):
    if version not in AGS_EDITOR_VALIDATED_DATA_CONTENTS.keys():
        return False
    return validate_file(filepath, os.path.basename(filepath),
                         AGS_EDITOR_VALIDATED_DATA_CONTENTS[version])
