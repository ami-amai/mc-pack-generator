import sys
import shutil
from pathlib import Path
import zipfile

from utils import ROOT
import utils

from pack import Pack

"""
Class
variable
COSTANT
is_boolean

"""

def is_json (str: str) -> bool:
    return str.find(".json") != -1

class MainPath(dict):

    def __init__(self, iterable):

        self.pack = Pack(iterable)

        # Paths
        ## Current output folder
        self.OUTPUT = ROOT.get('output', self.pack.AUTHOR, self.pack.ID, self.pack.VERSION)

        ## Curent pack source folder
        self.SOURCE = ROOT.get('pack', self.pack.ID)

        ## Current archive folders
        self.EXTRACTED_ARCHIVE = self.OUTPUT / 'extracted'
        self.ARCHIVE = self.OUTPUT / f'{self.pack.ID}-{self.pack.VERSION}.zip'

        ## Current names folder
        self.NAMES = self.OUTPUT / 'names/'

def create_path(data):

    path = MainPath(data)

    utils.mkdir(path.OUTPUT)
    utils.mkdir(path.EXTRACTED_ARCHIVE)
    utils.mkdir(path.NAMES)
    

def create_archive(data):

    pack = Pack(data)
    path = MainPath(data)

    # Open archive
    with zipfile.ZipFile(path.ARCHIVE, "w", zipfile.ZIP_DEFLATED) as archive:

        # Write Mcmeta
        archive.writestr("pack.mcmeta", pack.MCMETA)

        # Import files and targets
        for source, targets in pack.FILEDATA.items():
            for target in targets:
                # Add file
                ## Add Icon
                if target == "pack.png":
                    archive.writestr(target, pack.ICON)
                else:
                    # Add other files
                    archive.write(path.SOURCE / source, target)

        # Extract archive
        archive.extractall(path.EXTRACTED_ARCHIVE)

        print(f'Archive in {path.ARCHIVE}')
        print(f'Extracted in {path.EXTRACTED_ARCHIVE}')
        print()

def create_name(data):

    pack = Pack(data)
    path = MainPath(data)

    # Copy archive with different names
    print('Named archives:')
    for name in pack.NAMEDATA:
        NAMED_ARCHIVE = path.NAMES / f'{name}.zip' 
        shutil.copy(path.ARCHIVE, NAMED_ARCHIVE)
        print(f'{name}: {NAMED_ARCHIVE}')

def main():

    # Clear ./output dir
    OUTPUT = ROOT.get('output') 
    utils.rmdir(OUTPUT)
    utils.mkdir(OUTPUT)

    # Make ./pack/ folder if not exist
    utils.mkdir(ROOT.get('pack'))

    for arg in sys.argv:
        if is_json(arg):

            # Data and pack ID
            arg = Path(arg)
            data = utils.json_load(arg)

            create_path(data)
            create_archive(data)
            create_name(data)

if __name__ == "__main__":
    main()