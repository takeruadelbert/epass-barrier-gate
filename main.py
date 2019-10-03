from src.HID import *
from InputDeviceDev import *
from os import access, R_OK
from time import sleep
from src.config import retry_connect

def main():
    input_device = InputDeviceDev()
    rfid_devices = input_device.get_rfid_reader_device()
    if len(rfid_devices) > 0 and rfid_devices is not None:
        checkAccessOK = False
        for device_path, device_name in rfid_devices.items():
            # check if HID is readable
            if access(device_path, R_OK) :
                checkAccessOK = True
            else :
                err_message = "File '{}' isn't readable".format(device_path)
                print(err_message)
                break
        if checkAccessOK:
            hid = HID([*rfid_devices])
            if not hid.read_input():
                main()
    else :
        err_message = "No RFID Device found. Set Device Permission to readable."
        print(err_message)
        reconnect()
        
def reconnect():
    x = retry_connect
    while(x >= 1):
        print("Retrying to connect RFID Device(s) in " + str(x) + " second ...")
        sleep(1)
        x -= 1
    print()
    main()

if __name__ == "__main__" :
    main()