#!/bin/python3
# View and run Key Mapper actions using intents

import os
import json
import subprocess
import sys
import zipfile

path_to_keymapper_backup = '/storage/emulated/0/keymapper_backups/automatic/keymapper_mappings.zip'

def open_zip(zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        return zip_ref.read('data.json').decode('utf-8')

def parse_json(json_data):
    return json.loads(json_data)

def create_name_from_action_list(action_list):
    """Returns unique name consisting of the list of actions of a keymap. For KEY_EVENTs, android keycode numbers are replaced with names"""
    android_keycodes = json.load(open('android_keycodes.json'))
    result = ""
    for action in action_list:
        action_type = action['type']
        action_data = action['data']
        if action_type == 'KEY_EVENT':
            keycode = action_data
            for key, value in android_keycodes['keycodes'].items():
                if value == str(keycode):
                    result += f"KEY_EVENT_{key.upper()}_"
                    break
        else:
            result += f"{action['type']}_{action['data'].upper()}_"
    result=result.rstrip("_")
    return result.strip()

def get_intentable_keymaps(keymap_list):
    """Returns a dictionary containing names and uids of key maps that can be triggered by intent"""
    intentable_keymaps = {}
    keymap_triggered_by_intent_flag = 8 # from data.json
    for item in keymap_list:
        if item['trigger']['flags'] == keymap_triggered_by_intent_flag:
            action_list = item['actionList']
            name = create_name_from_action_list(action_list)
            uid = item['uid']
            intentable_keymaps[name] = uid
    return intentable_keymaps

def send_intent_by_name(names):
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_vars = dict(line.strip().split('=') for line in f)
        for name in names:
            if name in env_vars:
                uid = env_vars[name]
                command = f"am broadcast -n io.github.sds100.keymapper/io.github.sds100.keymapper.api.TriggerKeyMapsBroadcastReceiver -a io.github.sds100.keymapper.ACTION_TRIGGER_KEYMAP_BY_UID --es io.github.sds100.keymapper.EXTRA_KEYMAP_UID {uid}"
                subprocess.run(command, shell=True)
            else:
                print(f"Keymap {name} not found in .env file")
    else:
        json_file = open_zip(path_to_keymapper_backup)
        keymap_data = parse_json(json_file)
        keymap_list = keymap_data['keymap_list']
        intentable_keymaps = get_intentable_keymaps(keymap_list)
        for name in names:
            if name in intentable_keymaps:
                uid = intentable_keymaps[name]
                command = f"am broadcast -n io.github.sds100.keymapper/io.github.sds100.keymapper.api.TriggerKeyMapsBroadcastReceiver -a io.github.sds100.keymapper.ACTION_TRIGGER_KEYMAP_BY_UID --es io.github.sds100.keymapper.EXTRA_KEYMAP_UID {uid}"
                subprocess.run(command, shell=True)
            else:
                print(f"Keymap {name} not found")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--print-keymaps-json', action='store_true')
    parser.add_argument('--print-keymaps-names', action='store_true')
    parser.add_argument('--print-keymaps-uids', action='store_true')
    parser.add_argument('--run-keymap', type=str)
    parser.add_argument('--create-env-file', action='store_true')
    args = parser.parse_args()

    json_file = open_zip(path_to_keymapper_backup)
    keymap_data = parse_json(json_file)
    
    if args.print_keymaps_json:
        import pprint
        pprint.pprint(keymap_data)

    if args.print_keymaps_names:
        keymap_list=keymap_data['keymap_list']
        intentable_keymaps = get_intentable_keymaps(keymap_list)
        if args.print_keymaps_uids:
            for name, uid in intentable_keymaps.items():
                print(f"{name}={uid}")
        else:
            for name, uid in intentable_keymaps.items():
                print(f"{name}")

    if args.create_env_file:
        keymap_list = keymap_data['keymap_list']
        intentable_keymaps = get_intentable_keymaps(keymap_list)
        with open('.env', 'w') as f:
            for name, uid in intentable_keymaps.items():
                f.write(f"{name}={uid}\n")

    if args.run_keymap:
        send_intent_by_name(args.run_keymap.split(','))
