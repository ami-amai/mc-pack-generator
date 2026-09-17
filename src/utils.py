from pathlib import Path
import json

# Get data from file
def json_load (path):
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Mkdir
def mkdir(path: Path):
    path.mkdir(parents=True, exist_ok=True)