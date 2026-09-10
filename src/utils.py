from pathlib import Path
import json

# Get data from file
def json_load (path):
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def json_print (data):
    return json.dumps(data, ensure_ascii=False, indent=2)

# Mkdir
def mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)

# Root path
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