import utils
from utils import ROOT

import json

from pathlib import Path
from io import BytesIO
from PIL import Image

class Pack(dict):

    # Set Pack values with Init
    def __init__(self, iterable):
        # Data
        self.DATA = iterable

        # First level of Data
        self.METADATA = iterable["metadata"]
        self.FILEDATA = iterable["filedata"]
        self.NAMEDATA = iterable["namedata"]

        # Metadata
        self.TYPE = self.METADATA["type"]
        self.NAME = self.METADATA["name"]
        self.AUTHOR = self.METADATA["author"]
        self.ID = self.METADATA["id"]
        self.VERSION = self.METADATA["version"]
        self.FORMAT = self.METADATA["format"]
        self.FORMAT_VERSION = []

        # Filedata
        self.SOURCES = []

        # Mcmeta
        self.MCMETA = {}

        # Icon
        self.ICON = []

        # Functions
        self.format_version()
        self.namedata(iterable)
        self.mcmeta()
        self.filedata_sources()
        self.icon()

    def namedata(self, iterable):
        values = {
        "{name}": self.NAME,
        "{type}": self.TYPE,
        "{id}": self.ID,
        "{version}": self.VERSION,
        "{author}": self.AUTHOR,
        "{format.min}": self.FORMAT[0],
        "{format.max}": self.FORMAT[1],
        "{version.min}": self.FORMAT_VERSION[0],
        "{version.max}": self.FORMAT_VERSION[1],
        }

        names = self.NAMEDATA
        self.NAMEDATA = []
        for name in names:
            for old, new in values.items():
                name = str(name).replace(old, str(new))
            self.NAMEDATA.append(name)

    def format_version(self):
        type_file: Path = ROOT.get('src', 'json', 'type', f'{self.TYPE}.json')
        type_data: dict = utils.json_load(type_file)

        def get_version(index):
            return type_data[str(self.FORMAT[index])][index]

        min_version = get_version(0)
        max_version = get_version(1)

        if type_file.exists:
            self.FORMAT_VERSION.append(min_version)
            self.FORMAT_VERSION.append(max_version)
        else:
           self.FORMAT_VERSION = ["0", "0"]

    def mcmeta(self):
        self.MCMETA = json.dumps(
        # pack.mcmeta
        {
            "pack": {
                "pack_format": self.FORMAT[0],
                "description": [
                    {
                        "text": f"{self.ID}: {self.VERSION}",
                        "color": "white"
                    },
                    {
                        "text": f"\nby {self.AUTHOR}",
                        "color": "gray"
                    },
                ]
            },
            "supported_formats": [int(self.FORMAT[0]), int(self.FORMAT[1])]  
        },
        # json.dumps options
        ensure_ascii=False, indent=2)

    def filedata_sources(self):
        for key in dict(self.FILEDATA).keys():
            self.SOURCES.append(key)

    def icon(self) -> BytesIO:

        def image_to_buffer(image: Image) -> BytesIO:
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            return buffer.getvalue()

        def resize_image(path: Path, size: tuple) -> Image:
            with Image.open(path) as image:
                return image.resize((size[0],size[1]), resample=Image.Resampling.NEAREST)

        for source, targets in self.FILEDATA.items():
            icon_path = ROOT.get('pack', self.ID, source)
            for target in targets:
                if target == "pack.png":
                    icon = resize_image(icon_path, (256, 256))
                    self.ICON = image_to_buffer(icon)



