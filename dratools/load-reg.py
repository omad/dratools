"""
Hacky way to load a .reg file into the registry when regedit.exe has been disabled by the administrator

Probably very fragile!
"""

import sys

import winreg


def load_reg(input_file):
    lines = open(input_file, encoding='utf-16-le').read().splitlines()

    hkey = None
    for line in lines:
        if line.startswith('[HKEY'):
            hkey = line[1:-1]
            toplevel, sub_key = hkey.split('\\', maxsplit=1)
            top = getattr(winreg, toplevel)
            hkey = winreg.CreateKey(top, sub_key)
            print(f'inkey: {hkey}')
            continue
        if hkey is None:
            continue
        # Parse and load
        name, value = line.split('=')
        name = name.replace('"', '')
        value = value.replace('"', '')
        winreg.SetValueEx(hkey, name, 0, winreg.REG_SZ, value)


if __name__ == '__main__':
    filename = sys.argv[1]

    load_reg(filename)
