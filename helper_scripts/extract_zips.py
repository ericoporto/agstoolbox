import zipfile
import glob
import os
from pathlib import Path

###
### Do not run unless you know what you are doing
### This means you the author too
###
### When you are reaaaally sure you understand, remove 'exit' below
###
exit()

zip_files = []

for file in glob.glob("**/*.zip", recursive = True):
    zip_files.append(file)
    
for z in zip_files:
    z_path = Path(z)
    basename = z_path.stem
    basedir = z_path.parent
    dest_dir = os.path.join(basedir, basename)
    os.mkdir(dest_dir)
    a_zip = zipfile.ZipFile(z)
    a_zip.extractall(path=dest_dir)
    
