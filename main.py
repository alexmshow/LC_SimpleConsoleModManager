import logging
import packer
from mod import Mod

logging.basicConfig(level=logging.INFO)

def console():
    while (True):
        inp = input("ModManager> ")
        match inp:
            case "help":
                print("All commands: \n  * install - Install mods\n  * url     - Download from URL\n  * file    - Read from file\n  * exit    - Exit")
            case "url":
                mod = Mod.from_url(input("URL> "))
                mod.start()
                packer.clear()
                packer.sort_dirs()
            case "file":
                with open(input("FILE> "), "r") as f:
                    data = f.read()
                modurls = data.split("\n")
                for modurl in modurls:
                    mod = Mod.from_url(modurl)
                    mod.start()
                packer.clear()
                packer.sort_dirs()
            case "install":
                packer.install(input("GAME_DIR> "))
            case "exit":
                break

if __name__ == "__main__":
    console()