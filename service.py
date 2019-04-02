from pathlib import Path
import subprocess

# init variable
service_path_temp = "/lib/systemd/system/epass/epass.service"
service_path = "/lib/systemd/system/epass.service"

def create_service():    
    if check_file_exist():
        print("\n===============================================================================")
        print("Service 'epass.service' already exists in", "'" + service_path + "'.\nAborted.")
        print("===============================================================================\n")
    else:
        f = open(service_path_temp, "w+")
        content = "[Unit]\nDescription=E-Pass Barrier Gate for Member\nAfter=multi-user.target\n\n[Service]\nType=simple\nExecStart=/usr/bin/python3 /home/pi/Documents/python/epass-barrier-gate/main.py\nRestart=on-abort\n\n[Install]\nWantedBy=multi-user.target"
        f.write(content)
        f.close()
        
        subprocess.call(["sudo", "mv", service_path_temp, service_path])
        
        print("\n=============================================")
        print("File 'epass.service' is successfully created.")
        print("=============================================\n")

def check_file_exist():
    service_file = Path(service_path)
    if service_file.is_file():
        return True
    else:
        return False

if __name__ == "__main__":
    create_service()