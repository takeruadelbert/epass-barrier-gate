from src.HID import *

from os import access, R_OK

if __name__ == "__main__" :
    # check if HID is readable
    if access(hid_path, R_OK) :
        hid = HID()
        hid.read_input()
    else :
        err_message = "File '{}' isn't readable".format(hid_path)
        print(err_message)