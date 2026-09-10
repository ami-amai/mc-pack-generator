# Minecraft Pack Generator

* My personal python script for generation resourcepacks and datapacks

## Content

* Description
* JSON structure
    * Template
    * Placeholders
    * Example
* Usage

## Description

* This generator uses JSON files for generating packs from sources
* You need to get or create special JSON for using this script

## JSON Structure

### Template:

```json
{
    "id": {
        "name": "Pack name",
        "version": "Pack version",
        "icon": "<path_to_icon>",
        "metadata": {
            "description": "Description",
            "author": "Username",
            "format": [ 0, 88 ],
            "version": [ "1.0", "26.2" ]
        },
        "files": {
            "<path_to_file>": {
                "arcnames": [
                    "<path_inside_archive>",
                ],
                "targets": [
                    "<name_of_archive>"
                ]
            }
        }
    }
}
```
* JSON can have many packs
* JSON can use absolute and relative paths
* Packs can have many files with their own arcnames and targets
* Files has priority above pack.mcmeta and pack.png

### Placeholders

* Some values have placeholders:
    * `id.name`
    * `id.version`
    * `id.metadata.description`
    * `id.metadata.author`
    * `id.files.<file>.targets.<target>`

* Placeholders:
    * {id} - `id`
    * {name} - `id.name`
    * {version} - `id.version`
    * {meta.author} - `id.metadata.author`
    * {meta.format.min} - `id.metadata.format[0]`
    * {meta.format.max} - `id.metadata.format[1]`
    * {meta.version.min} - `id.metadata.version[0]`
    * {meta.version.max} - `id.metadata.version[1]`

*P.s - Recursion can break pack*

### Example

```json
{
    "example": {
        "name": "Example pack",
        "version": "1.0",
        "icon": "./example/pack.png",
        "metadata": {
            "description": "This is example pack: {id}",
            "author": "Ami_Amai",
            "format": [ 87, 88 ],
            "version": [ "26.2", "26.2" ]
        },
        "files": {
            "./example/pack.png": {
                "arcnames": [
                    "assets/minecraft/textures/item/paper.png"
                ],
                "targets": [
                    "{name}_{version}"
                ]
            }
        }
    }
}
```

* Example will create `./output/Ami_Amai/example/1.0/Exmple pack_1.0.zip` with:
    * `pack.mcmeta`
        * `pack_format = 87`
        * description:
            * `This is example pack: example`
            * `Ami_Amai`
        * `supported_formats = [87, 88]`
    * `pack.png` from `./example/pack.png` with 128x128 size
    * `assets/minecraft/textures/item/paper.png` from `./example/pack.png`
* Also example will create extracted archive inside `./output/Ami_Amai/example/1.0/Exmple pack_1.0`

## Usage

1. Create VENV inside repository

```bash
python -m venv .venv
```

2. Install requirements inside .venv

```bash
.venv/bin/pip -r requirements
```

3. Launch script with selected JSON

```bash
.venv/bin/python src/main.py <file1> <file2> ...
```