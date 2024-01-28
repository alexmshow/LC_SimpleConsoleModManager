import os, shutil, zipfile

try: os.makedirs("./temp")
except FileExistsError: ...

try: os.makedirs("./mods/plugins")
except FileExistsError: ...

try: os.makedirs("./mods/config")
except FileExistsError: ...

def check_file(filepath):
    return os.path.exists(filepath)

def unpack(filepath, out):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(out)

def remfile(filepath):
    try: os.remove(filepath)
    except FileNotFoundError: ...