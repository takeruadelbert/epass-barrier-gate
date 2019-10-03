from src.config import hid_name

import evdev

class InputDeviceDev :
    def __init__(self):
        self.devices = [evdev.InputDevice(hid_path) for hid_path in evdev.list_devices()]
        self.input_devices = self.get_all_input_devices()        

    def print_all_input_devices(self):
        for device in self.devices :
            print(device.path, device.name, device.phys)

    def get_all_input_devices(self):
        input_devices = {}
        for device in self.devices:
            input_devices[device.path] = device.name
        return input_devices

    def get_rfid_reader_device(self):
        rfid_devices = {}
        if len(self.input_devices) > 0 :
            for device_path, device_name in self.input_devices.items() :
                if hid_name not in device_name:
                    continue
                else:
                    rfid_devices[device_path] = device_name
            return rfid_devices
        else:
            print("No Device(s) found.")
            return ""