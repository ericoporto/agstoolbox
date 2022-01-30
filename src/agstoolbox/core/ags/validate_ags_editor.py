import os
import hashlib


from agstoolbox.core.ags.ags_editor_validation_data import \
    AGS_EDITOR_VALIDATED_DATA_ZIP, AGS_EDITOR_VALIDATED_DATA_CONTENTS

BUF_SIZE = 131072


def validate_file(z_file, validation_data):
    if z_file not in validation_data:
        return False

    if not os.path.exists(z_file):
        return False

    if os.path.isdir(z_file):
        return False

    if os.path.getsize(z_file) != validation_data[z_file]['size']:
        return False

    md5_checker = hashlib.md5()
    with open(z_file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5_checker.update(data)

    return md5_checker.hexdigest() == validation_data[z_file]['md5']


def validate_ags_editor_zip(z_file):
    return validate_file(z_file, AGS_EDITOR_VALIDATED_DATA_ZIP)


def validate_editor_contents(file):
    return validate_file(file, AGS_EDITOR_VALIDATED_DATA_CONTENTS)
