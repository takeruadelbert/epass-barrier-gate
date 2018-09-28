from src.config import *
from time import sleep

import requests
import socket
import fcntl
import struct
import re
import platform
import datetime

class BarrierGate :
    def get_ip_address(self, ifname=''):
        if platform.system() == "Linux" :
            ifname = "enp3s0"
        else :
            ifname = "eth0"
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

    def main(self):
        while 1 :
            dt = self.get_current_datetime()
            code = str(input(dt + " Scan Code : "))
            input_code = re.sub(r"\W", "", code).replace("B", "")
            if code != "" :
                self.check_out(input_code)
            else :
                print("Invalid Code")
            print("\n")