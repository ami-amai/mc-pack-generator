import utils
from pack import Pack
from utils import ROOT

import sys
import json
import zipfile
import shutil

from pathlib import Path

class MainPath(Pack):

    def __init__(self, iterable):
        self.OUTPUT = ROOT.get('output', iterable.META_AUTHOR, iterable.ID, iterable.VERSION)

    def ARCHIVE (self, target: str):
        return self.OUTPUT / f'{target}.zip'
    
    def EXTRACT (self, target: str):
        return self.OUTPUT / target

    def SOURCE (self, source: str):
        return Path(source).resolve()

def main():

    shutil.rmtree(ROOT.get('output'),ignore_errors=True)

    for i, arg in enumerate(sys.argv):
        if i != 0:
            data = utils.json_load(ROOT.get(arg))
            for pack in data.items():

                # Get Pack() class
                pack = Pack(pack)

                # Get MainPath() class
                path = MainPath(pack)

                utils.mkdir(path.OUTPUT)

                for file in pack.FILES:
                    with zipfile.ZipFile(path.ARCHIVE(file["target"]), "w", zipfile.ZIP_DEFLATED) as archive:

                        # Add icon and mcmeta
                        archive.writestr("pack.mcmeta", pack.MCMETA)
                        archive.writestr("pack.png", pack.ICON)

                        # Add file
                        archive.write(path.SOURCE(file["source"]), file["arcname"])

                        # Extract files
                        EXTRACT = path.EXTRACT(file["target"])
                        utils.mkdir(EXTRACT)
                        archive.extractall(EXTRACT)

if __name__ == "__main__":
    main()