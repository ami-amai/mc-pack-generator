# Minecraft pack generator

* This is python script for generating resourcepacks and datapacks with special JSON

## JSON

* For using generator you need to get or create json file

### Example

```json
{
    "config": {
        "pack.description": "Description",
        "pack.author": "author",
        "pack.format": [ 1, 88 ],
        "my.name": "pack"
    },
    "files": {
        "{pack.folder}/image.png": [
            [ "pack.png" ],
            [ "{pack.folder}/{my.name}" ]
        ]
    }
}
```

* `config` contains some usable variables, you can create your vars
    * You can use them with {key} or {key:index} if list
    * If {key} is list - current value will be split to all possible variants
    * Special variables:
        * `pack.description` - description inside pack.mcmeta, the first row
        * `pack.author` - description inside pack.mcmeta, "by {pack.author}", the second row
        * `pack.format` - `[ min, max ]`, pack_format inside pack.mcmeta
        * `pack.folder` - returns absolute path to this json, if not overrided
* `files` contains information about files
    * Structure -
        ```json
        "path_to_source": [ [ "paths_inside_archive" ], [ "paths_to_archives" ] ]
        ```
    * Any source can be placed in a few archives with a few names inside

## Usage

1. Create VENV with python:
```bash
pythom -m venv .venv/
```

2. Activate VENV:
```bash
source .venv/bin/activate
```

3. Install requirements:
```bash
.venv/bin/pip install -r src/requirements.txt
```

4. Use script with file path as argument:
```bash
.venv/bin/python src/main.py pack/pack.json
```

* All packs will be created as archives
