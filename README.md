# KeyMapPy
Currently in beta.

Trigger your [Key Mapper](https://github.com/keymapperorg/KeyMapper) key maps by the list of actions that they perform. Uses key maps that have "Allow other apps to trigger this key map" enabled. 

## Setup
1. Clone thus repo into `/data/data/com.termux/files/home/.local/lib/python3.12/site-packages/`
2. Set up Key Mapper's `Automatically back up mappings to a specified location`
3. Change this line of __init__.py to the path to your backup zip file:

```
path_to_keymapper_backup = '/storage/emulated/0/keymapper_backups/automatic/keymapper_mappings.zip'
```

## Usage:

```
$ python __init__.py --help
usage: __init__.py [-h] [--print-keymaps-json] [--print-keymaps-names]                                      [--print-keymaps-uids] [--run-keymap RUN_KEYMAP] [--create-env-file]                                                                                           options:
  -h, --help            show this help message and exit                                    --print-keymaps-json
  --print-keymaps-names                                                                    --print-keymaps-uids
  --run-keymap RUN_KEYMAP                                                                  --create-env-file
```

