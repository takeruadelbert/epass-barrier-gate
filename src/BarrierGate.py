from src.config import ip_address_server, url, timeout_connection, retry_connect
from time import sleep

import requests
import socket
import fcntl
import struct
import re
import datetime
import io

class BarrierGate :
    def get_ip_address(self, ifname=''):
        if self.is_raspberry_pi() :
            ifname = "eth0"
        else :
            ifname = "enp3s0"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip_address = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
        return str(ip_address)

    def retry_connect(self):
        x = retry_connect
        while(x >= 1) :
            print("Retrying connect to server in " + str(x) + " second ...")
            sleep(1)
            x -= 1
        print("Reconnecting ...")
        self.main()

    def check_out(self, code):
        try :
            par = {
                'code': code,
                'ip': self.get_ip_address()
            }
            full_url = ip_address_server + url
            response = requests.post(full_url, json=par, timeout=timeout_connection)
            response.raise_for_status()
            response_data = response.json()
            print(self.get_current_datetime() + " " + response_data['message'])
        except requests.exceptions.ConnectionError :
            print("Cannot establish connection to server, please setup the server properly.")
            self.retry_connect()
        except requests.exceptions.Timeout as err_timeout :
            print(err_timeout)

            self.retry_connect()
        except requests.exceptions.HTTPError as err_http :
            print(err_http)
            self.retry_connect()

    def get_current_datetime(self):
        return "[" + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S") + "]"

    def is_raspberry_pi(self, raise_on_errors = False):
        try:
            with io.open('/proc/cpuinfo', 'r') as cpuinfo:
                found = False
                for line in cpuinfo:
                    if line.startswith('Hardware'):
                        found = True
                        label, value = line.strip().split(':', 1)
                        value = value.strip()
                        if value not in (
                                'BCM2708',
                                'BCM2709',
                                'BCM2835',
                                'BCM2836'
                        ):
                            if raise_on_errors:
                                raise ValueError(
                                    'This system does not appear to be a '
                                    'Raspberry Pi.'
                                )
                            else:
                                return False
                if not found:
                    if raise_on_errors:
                        raise ValueError(
                            'Unable to determine if this system is a Raspberry Pi.'
                        )
                    else:
                        return False
        except IOError:
            if raise_on_errors:
                raise ValueError('Unable to open `/proc/cpuinfo`.')
            else:
                return False
        return True