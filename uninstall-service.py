from pathlib import Path
import subprocess

# init variable
service_name = "epass.service"
service_path = "/lib/systemd/system/epass.service"

def uninstall_service():    
    if check_file_exist():         
        subprocess.call(["sudo", "systemctl", "stop", service_name])
        subprocess.call(["sudo", "systemctl", "disable", service_name])
        subprocess.call(["sudo", "systemctl", "daemon-reload"])
        subprocess.call(["sudo", "systemctl", "reset-failed"])
        subprocess.call(["sudo", "rm", service_path])
        print("\n=======================")
        print("Uninstall Successfully.")
        print("=======================\n")
    else:
        print("\n=======================")
        print("Service doesn't exists.")
        print("=======================\n")

def check_file_exist():
    service_file = Path(service_path)
    if service_file.is_file():
        return True
    else:
        return False

if __name__ == "__main__":
    uninstall_service()
