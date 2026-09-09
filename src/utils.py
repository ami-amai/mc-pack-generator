import json
from pathlib import Path
import shutil

class Root(str):

    def __init__(self, *args):
        # Project Dir
        self.ROOT = Path(args[0])

    def get (self, *args):
        path = self.ROOT
        for arg in args:
            path = path / arg
        return path

ROOT = Root(Path(__file__).resolve().parents[1])

# Create files and dirs
## Touch
def touch(path: Path):
    mkdir(path.parent)
    path.touch(exist_ok=True)

# MkDir
def mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

def rmdir(path: Path):
    if path.exists:
        shutil.rmtree(path, ignore_errors=True)
    else:
        pass

# JSON
## Import
def json_load (path):
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data
