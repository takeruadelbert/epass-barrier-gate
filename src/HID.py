from src.DataMapASCIICode import capscodes, scancodes
from src.BarrierGate import *
from InputDeviceDev import *
from evdev import InputDevice, categorize, ecodes

from select import select

class HID:
    def __init__(self, rfid_path_devices):        
        if rfid_path_devices != "":
            self.map_device(rfid_path_devices)
            self.barrierGate = BarrierGate()
        else:
            self.err = True
            self.err_message = "No RFID Device found."
            
    def map_device(self, rfid_path_devices):
        self.device = map(InputDevice, rfid_path_devices)
        self.device = {dev.fd : dev for dev in self.device}
    
    def read_input(self):
        try:
            code = ''
            caps = False

            dt = self.barrierGate.get_current_datetime()
            print(dt + " Scan Code : ", end='', flush=True)

            # loop
            while True:
                r,w,x = select(self.device, [], [])
                for fd in r:
                    for event in self.device[fd].read():                
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
                                    if code != "":
                                        self.barrierGate.check_out(code)  # call the API function to server
                                    else:
                                        print("Invalid Code")
                                    code = ''
                                    dt = self.barrierGate.get_current_datetime()
                                    print("\n" + dt + " Scan Code : ", end='', flush=True)
        except KeyboardInterrupt:
            print("\nProgram is exit.")
        except OSError:
            print("\nDevice is disconnected.")
            return False
