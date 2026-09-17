
"""
Minecraft Pack Class

Pack() contains all information from given data

"""

# Imports
import utils

from io import BytesIO
from pathlib import Path
from PIL import Image
from itertools import product
from collections import defaultdict

import json
import itertools
import re

class Pack():

    def __init__(self, path: Path):

        self.FILE = path.resolve()
        self.FOLDER = path.resolve().parent

        self.tags = PackTag(self, self.get_config_tags())
        self.files = PackFile(self, self.get_config_files())

        self.mcmeta()

    def get_data(self):
        return utils.json_load(self.FILE)

    def get_config_tags(self):
        return self.get_data()["config"]

    def get_config_files(self):
        return self.get_data()["files"]

    def mcmeta(self):
        self.MCMETA = json.dumps(
        # pack.mcmeta
        {
            "pack": {
                "pack_format": int(self.tags.apply('{pack.format:0}')[0]),
                "description": [
                    {
                        "text": self.tags.apply('{pack.description}')[0],
                        "color": "white"
                    },
                    {
                        "text": f"\nby {self.tags.apply('{pack.author}')[0]}",
                        "color": "gray"
                    },
                ]
            },
            "supported_formats": [int(self.tags.apply('{pack.format:0}')[0]), int(self.tags.apply('{pack.format:1}')[0])]  
        },
        # json.dumps options
        ensure_ascii=False, indent=2)

    def icon(self, arg: str) -> BytesIO:

        absolute_path = Path(arg).resolve()
        buffer = BytesIO()

        with Image.open(absolute_path) as image:
            image = image.resize((128, 128), resample=Image.Resampling.NEAREST)
            image.save(buffer, format='PNG')

        return buffer.getvalue()

class PackTag():

    def __init__(self, pack: Pack, data):

        self.pack = pack
        self.DATA = data
        
        self.LIST = {}
        self.init()

    # Init and Create default tags
    def init(self):
        # Default
        default = {
            "pack.folder": self.pack.FOLDER,
            "pack.description": "description",
            "pack.author": "author",
            "pack.format": [ 1, 999 ]}.items()

        for key, value in default:
            if self.LIST.get(key) == None:
                self.append(key, value)

        # Pack
        for key, value in self.DATA.items():
            self.append(key, value)

    # Append tag to List of tags
    def append(self, key, value: str | list):
        self.LIST[key] = value

    # Find all Tags in str
    def find(self, _str: str):
        found = {}
        pattern = re.findall(r'(\{([^{}:]+)(?::([^{}:]+))?\})', _str)
        
        while (pattern != None) and (len(pattern) > 0):
            p = pattern.pop(0)
            found[p[0]] = [ p[1], p[2]]

        return found if len(found) > 0 else None

    # Apply tags to str
    def apply(self, _str: str):

        found = self.find(_str)
        if found is None:
            return [_str]

        tags = list(found.keys())

        def _resolve(key, index):
            value = self.LIST.get(key)
            
            if value == None:
                return [ f'{{{key}}}']
            if index:
                return [value[int(index)]]
            return value if isinstance(value, list) else [value]
    
        value_lists = [_resolve(key, index) for key, index in found.values()]

        results = []
        for item in product(*value_lists):
            replaced = _str
            for tag, value in zip(tags, item):
                replaced = replaced.replace(tag, str(value))

            results.append(replaced) if replaced == _str else results.extend(self.apply(replaced))
        return results

class PackFile():

    def __init__(self, pack: Pack, data):

        self.pack = pack
        self.DATA = data

        self.LIST = []
        self.init()

    # Create list of files
    def init(self):
        result = defaultdict(list)

        def apply (_str):
            return self.pack.tags.apply(_str)

        for source, (arcnames, targets) in self.DATA.items():

            def _apply_to_list (list: list):
                result = []
                for item in list:
                    result.extend(apply(item))
                return result

            _sources = apply(source)
            _arcnames = _apply_to_list(arcnames)
            _targets = _apply_to_list(targets)

            # Для каждой цели собираем все возможные [source, arcname]
            for t in _targets:
                for s, a in product(_sources, _arcnames):
                    pair = [s, a]
                    if pair not in result[t]:
                        result[t].append(pair)

        self.LIST = dict(result)
