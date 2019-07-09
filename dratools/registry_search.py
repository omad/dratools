from contextlib import suppress
from winreg import OpenKey, EnumKey, QueryInfoKey, HKEY_CURRENT_USER


def subkeys(hkey=HKEY_CURRENT_USER, path='', accum=''):
    with suppress(WindowsError), OpenKey(hkey, path) as k:
        nsubkeys, nvalues, _ = QueryInfoKey(k)
        # for i in range(nvalues):
        #     yield winreg.EnumValue(k, i)
        for i in range(nsubkeys):
            sub_key = EnumKey(k, i)
            fullpath = accum + '\\' + sub_key
            yield fullpath
            yield from subkeys(k, sub_key, fullpath)


for path in subkeys():
    if 'raijin' in path:
        print(path)
