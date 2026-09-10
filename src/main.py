import utils
from pack import Pack
from utils import ROOT

import sys
import json
import zipfile
import shutil

from pathlib import Path

def main():

    shutil.rmtree(ROOT.get('output'),ignore_errors=True)

    for i, arg in enumerate(sys.argv):
        if i != 0:
            data = utils.json_load(ROOT.get(arg))
            for item in data.items():
                item = Pack(item)

                output_path = ROOT.get('output', item.META_AUTHOR, item.ID, item.VERSION)
                utils.mkdir(output_path)

                for file in item.FILES:
                    archive_path = output_path / f'{file["target"]}.zip'
                    with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                        archive.write(Path(file["source"]).resolve(), file["arcname"])
                        archive.writestr("pack.mcmeta", item.MCMETA)
                        archive.writestr("pack.png", item.ICON)

                        extract_path = output_path / file["target"]
                        utils.mkdir(extract_path)
                        archive.extractall(extract_path)

if __name__ == "__main__":
    main()