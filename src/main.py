import utils

from pack import Pack
import os

import sys
import zipfile

from pathlib import Path


def main():

    # Get all packs
    for i, arg in enumerate(sys.argv):
        if i != 0:
            # Get pack data
            pack = Pack(Path(arg))

            # Get pack files
            files = pack.files.LIST.items()

            # Create archive and add files
            for target, pairs in files:
                zip_path = Path(f'{target}.zip')

                # Create output path if not exists
                if zip_path.parent.exists is False:
                    utils.mkdir(zip_path.parent)
                # Remove old archive if exists
                if Path(zip_path).exists():
                    os.remove(zip_path)
                with zipfile.ZipFile(f'{target}.zip', "a", zipfile.ZIP_DEFLATED) as archive:
                    # Add pack.mcmeta
                    archive.writestr("pack.mcmeta", pack.MCMETA)
                    for source, arcname in pairs:

                        # Add file if not in archive
                        if arcname not in archive.namelist():
                            # pack.png
                            if arcname == "pack.png":
                                archive.writestr(arcname, pack.icon(source))
                            # file
                            else:
                                archive.write(source, arcname)

if __name__ == "__main__":
    main()