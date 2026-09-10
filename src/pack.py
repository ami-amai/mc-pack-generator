import json
from io import BytesIO
from pathlib import Path

import utils
from utils import ROOT
from PIL import Image


class Pack(tuple):

    def __init__(self, iterable):

        # Get main values
        self.ID = iterable[0]
        self.DATA = iterable[1]

        # Data
        self.NAME = self.DATA["name"]
        self.VERSION = self.DATA["version"]
        self.METADATA = self.DATA["metadata"]
        self.FILEDATA = self.DATA["files"]

        # Metadata
        self.META_DESCRIPTION = self.METADATA["description"]
        self.META_AUTHOR = self.METADATA["author"]
        self.META_FORMAT = self.METADATA["format"]
        self.META_VERSION = self.METADATA["version"]

        # Files
        self.FILES = None

        # pack.mcmeta
        self.MCMETA = None

        # Placeholders
        self.NAME = self.placeholder(self.NAME)
        self.VERSION = self.placeholder(self.VERSION)

        self.META_AUTHOR = self.placeholder(self.META_AUTHOR)
        self.META_DESCRIPTION = self.placeholder(self.META_DESCRIPTION)

        # Functions
        self.files()
        self.mcmeta()
        self.icon()

# Placeholder for values
    def placeholder (self, value: str) -> str:
        placeholders = {
            "{id}": self.ID,
            "{name}": self.NAME,
            "{version}": self.VERSION,
            "{meta.author}": self.META_AUTHOR,
            "{meta.format.min}": self.META_FORMAT[0],
            "{meta.format.max}": self.META_FORMAT[1],
            "{meta.version.min}": self.META_VERSION[0],
            "{meta.version.max}": self.META_VERSION[1],
        }
        r = []
        for old, new in placeholders.items():
            value = str(value).replace(old, str(new))
        return value

    def files(self):
        files = []
        for source, data in self.FILEDATA.items():
            for arcname in data["arcnames"]:
                for target in data["targets"]:
                    files.append({
                        "source": source,
                        "arcname": arcname,
                        "target": self.placeholder(target)
                    })
        self.FILES = files

    def mcmeta(self):
            self.MCMETA = json.dumps(
            # pack.mcmeta
            {
                "pack": {
                    "pack_format": self.META_FORMAT[0],
                    "description": [
                        {
                            "text": f"{self.META_DESCRIPTION}",
                            "color": "white"
                        },
                        {
                            "text": f"\nby {self.META_AUTHOR}",
                            "color": "gray"
                        },
                    ]
                },
                "supported_formats": [int(self.META_FORMAT[0]), int(self.META_FORMAT[1])]  
            },
            # json.dumps options
            ensure_ascii=False, indent=2)

    def icon(self) -> BytesIO:

        def image_to_buffer(image: Image) -> BytesIO:
            buffer = BytesIO()
            image.save(buffer, format='PNG')
            return buffer.getvalue()

        def resize_image(path: Path, size: tuple) -> Image:
            with Image.open(path) as image:
                return image.resize((size[0],size[1]), resample=Image.Resampling.NEAREST)

        icon_path = Path(self.DATA["icon"]).resolve()
        icon = resize_image(icon_path, (128, 128))
        self.ICON = image_to_buffer(icon)
            
            