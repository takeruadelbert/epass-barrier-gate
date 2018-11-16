from src.HID import *
from InputDevice import *
from os import access, R_OK

if __name__ == "__main__" :
    # check if HID is readable
    input_device = InputDevice()
    device_path = input_device.get_rfid_reader_device()
    if device_path != "":
        if access(device_path, R_OK) :
            hid = HID(device_path)
            hid.read_input()
        else :
            err_message = "File '{}' isn't readable".format(device_path)
            print(err_message)
    else :
        err_message = "No RFID Device found."
        print(err_message)