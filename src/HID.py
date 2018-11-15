from src.config import hid_path
from src.DataMapASCIICode import capscodes, scancodes
from src.BarrierGate import *
from evdev import InputDevice, categorize, ecodes

class HID :
    def __init__(self):
        self.device = InputDevice(hid_path)
        self.barrierGate = BarrierGate()

    def read_input(self):
        try :
            code = ''
            caps = False

            # provides exclusive access to device
            self.device.grab()

            dt = self.barrierGate.get_current_datetime()
            print(dt + " Scan Code : ", end='', flush=True)

            # loop
            for event in self.device.read_loop():
                if event.type == ecodes.EV_KEY:
                    data = categorize(event)  # Save the event temporarily to introspect it
                    if data.scancode == 42:
                        if data.keystate == 1:
                            caps = True
                        if data.keystate == 0:
                            caps = False
                    if data.keystate == 1:  # Down events only
                        if caps:
                            key_lookup = u'{}'.format(capscodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                                data.scancode)  # Lookup or return UNKNOWN:XX
                        else:
                            key_lookup = u'{}'.format(scancodes.get(data.scancode)) or u'UNKNOWN:[{}]'.format(
                                data.scancode)  # Lookup or return UNKNOWN:XX
                        if (data.scancode != 42) and (data.scancode != 28):
                            code += key_lookup
                        if data.scancode == 28:
                            if code != "" :
                                print(code) # print received scanned input to terminal
                                self.barrierGate.check_out(code) # call the API function to server
                            else :
                                print("Invalid Code")
                            code = ''
                            dt = self.barrierGate.get_current_datetime()
                            print("\n" + dt + " Scan Code : ", end='', flush=True)
        except KeyboardInterrupt:
            print("\nProgram is exit.")