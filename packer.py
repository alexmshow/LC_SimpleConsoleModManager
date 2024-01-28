import directory

import os, shutil

DELETE_FILES = set(["readme.md", "changelog.md", "manifest.json", "icon.png", "license.txt", "license", "license.md", "installing.txt"])
TRUSTED_FOLDERS = set(["translation", "core", "bundles", "config", "core", "custom songs", "plugins", "patchers"])


def clear(folder="./mods/"):
    for file in os.listdir(folder):
        rel_path = folder + file 
        if file.lower() not in DELETE_FILES:
            continue
        directory.remfile(rel_path)

def sort_dirs(folder="./mods/"):
    for file in os.listdir(folder):
        if os.path.isdir(folder + file) and file.lower() == "bepinexpack":
            shutil.copytree(folder + "BepInExPack", folder, dirs_exist_ok=True)
            shutil.rmtree(folder + "BepInExPack")
            continue

        elif os.path.isdir(folder + file):
            if file.lower() == "bepinexpack":
                shutil.copytree(folder + "BepInExPack", folder, dirs_exist_ok=True)
                shutil.rmtree(folder + "BepInExPack")
            elif file.lower() == "bepinex":
                continue
            elif file.lower() in TRUSTED_FOLDERS:
                shutil.copytree(folder + file, folder + "BepInEx/" + file, dirs_exist_ok=True)
                shutil.rmtree(folder + file)
            elif file.lower() not in TRUSTED_FOLDERS:
                shutil.copytree(folder + file, folder + "BepInEx/" + "plugins/" + file, dirs_exist_ok=True)
                shutil.rmtree(folder + file)

        elif file == "winhttp.dll":
            continue
        elif file == "doorstop_config.ini":
            continue

        elif file.endswith(".dll"):
            shutil.copy(folder + file, folder + "BepInEx/" +"plugins/" + file)
            os.remove(folder + file)
        
        elif file.endswith(".cfg"):
            shutil.copy(folder + file, folder + "BepInEx/" + "config/" + file)
            os.remove(folder + file)
        else:
            shutil.copy(folder + file, folder + "BepInEx/" + "plugins/" + file)
            os.remove(folder + file)

def install(path):
    shutil.copytree("./mods", path, dirs_exist_ok=True)