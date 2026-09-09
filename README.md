# Minecraft Pack Generator

* This is my personal script for generating resourcepacks and datapacks for Minecraft from json

## Structure

* `./output/` - result of generating
* `./pack/` - for pack files
* `./src/` - python project
* `./README.md`
* `LICENSE` - license

## JSON

* You need to make JSON and add some files for your pack

## JSON structure

* Exmple
```
# ./pack/pack.json
{
    "metadata": {
        "type": "resourcepack",
        "name": "Pack",
        "author": "pack_author",
        "id": "packid",
        "version": "0.0.1",
        "format": [4, 88.0]
    },
    "filedata": {
        "pack.png": [
            "pack.png",
            "assets/minecraft/textures/item/paper.png"
        ]
    },
    "namedata": [
        "{name}",
        "{type}",
        "{id}",
        "{version}",
        "{author}",
        "{format.min}",
        "{format.max}",
        "{version.min}",
        "{version.max}"
    ]
}
```

* `metadata` - information about your pack
    * `type` - type of your pack (resourcepack / datapack)
    * `name` - pack name
    * `id` - pack id
    * `author` - your name
    * `version` - pack version
    * `format` - pack_format
* `filedata` - files that should be added to the pack
    * **key** - files from `./pack/ID/`
    * **values** - path inside archive
* `namedata` - custom archive names, has some placeholders
    * {type} = `metadata.type`
    * {name} = `metadata.name`
    * {author} = `metadata.author`
    * {id} = `metadata.id`
    * {version} = `metadata.version`
    * {format.min} = first `metadata.format`
    * {format.max} = second `metadata.format`
    * {version.min} = min version of `{format.min}` pack_format (1.13 from example)
    * {version.max} = max version of `{format.max}` pack_format (26.2 from example)

## Usage

1. **If you need - create venv**

* Create venv
```
python -m venv ./venv
```

* Activate venv
```
source ./.venv/bin/activate
```

2. **Install requirements**

```
pip install -r ./src/requirements.txt
```

3. **Launch script**
```
python src/main.py <path_to_pack_json> <paths_to_other_pack_jsons>
```
* Example
```
python src/main.py ./pack/pack.json
```