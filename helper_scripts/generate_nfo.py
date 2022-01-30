import os
import sys
import glob
import os
import hashlib
import json
from pathlib import Path

BUF_SIZE = 131072

md5 = hashlib.md5()

def dict_to_string(a_dict):
    return str(json.dumps(a_dict, sort_keys=True, indent=4))

cur_dir = Path(__file__).resolve().parent
base_dir = os.path.join(cur_dir, 'Vers')

AGS_EDITOR_VALIDATED_DATA_ZIP = {}

AGS_EDITOR_VALIDATED_DATA_CONTENTS = {}

for file in glob.glob("**/*.*", recursive = True):

    if os.path.isdir(file):
        continue

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            md5.update(data)

    hashed_file = {'size': os.path.getsize(file),
                   'md5' : md5.hexdigest()
                   }
                       
    rel_file_path = Path(os.path.relpath(file, base_dir)).as_posix()
    
    if file.endswith('.zip'):
        AGS_EDITOR_VALIDATED_DATA_ZIP[rel_file_path] = hashed_file
    else:
        top_dir = rel_file_path.split('/')[0]
        t = top_dir.split('.')
        vers = '0'
        if len(t) > 1:
            vers = t[1]
    
        if vers not in AGS_EDITOR_VALIDATED_DATA_CONTENTS:
            AGS_EDITOR_VALIDATED_DATA_CONTENTS[vers] = {}
            
            
        p = Path(rel_file_path)
        p_rel = str(Path(*p.parts[2:]))
        AGS_EDITOR_VALIDATED_DATA_CONTENTS[vers][p_rel] = hashed_file
    
    
    
print('AGS_EDITOR_VALIDATED_DATA_ZIP = ' + dict_to_string(AGS_EDITOR_VALIDATED_DATA_ZIP))
print("\n")
print('AGS_EDITOR_VALIDATED_DATA_CONTENTS = ' + dict_to_string(AGS_EDITOR_VALIDATED_DATA_CONTENTS))

