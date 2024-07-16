#!/usr/bin/python
import prefs
import string
from ctypes import windll
import os

def get_vrdDrives():
    # Returns a list of drives to import from. All drives on the system is checked
    # for the presence of drive:\foldername and if found this drive is added to the
    # list. Returns None if nothing is found.

    drives = []
    result = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter + ':\\')
        bitmask >>= 1

    for drive in drives:
        vrdPath = os.path.join(drive, prefs.DATABASE_DIRECTORY)
        isExist = os.path.exists(vrdPath)
        if isExist:
            result.append(os.path.abspath(vrdPath))
        
    return result

 
  
if __name__ == "__main__":
    print(get_vrdDrives())     #Lists all drives that matches the search for vrd drive. e.g. ['F://vrd_database']