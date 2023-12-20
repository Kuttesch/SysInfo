import subprocess
import sys

#def install(package):
#    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# List of required packages
#required_packages = ["psutil", "screeninfo", "py-cpuinfo", "gputil", "colorama"]

#for package in required_packages:
#    try:
#        # Try to import the package
#        __import__(package)
#    except ImportError:
#        # If the import fails, install the package
#        install(package)

import os
import platform
import psutil
from screeninfo import get_monitors
from cpuinfo import get_cpu_info
import GPUtil
import datetime
from colorama import Fore, Style

# Check the operating system
print(Fore.BLUE + "lllllll lllllll      ",     "OS:      ", Fore.WHITE + platform.system(), Style.RESET_ALL)

# Get the OS uptime
boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
uptime = datetime.datetime.now() - boot_time

days = uptime.days
hours, remainder = divmod(uptime.seconds, 3600)
minutes, _ = divmod(remainder, 60)

print(Fore.BLUE + "lllllll lllllll      ",     "Uptime:  ",   Fore.WHITE + "{} days, {} hours, {} minutes".format(days, hours, minutes), Style.RESET_ALL)

# Get the screen resolution
primary_monitor = get_monitors()[0]
print(Fore.BLUE + "lllllll lllllll      ",     "Screen: ", Fore.WHITE +"", primary_monitor.width, "*", primary_monitor.height, Style.RESET_ALL)

# Get the CPU information
print("                     ",    Fore.BLUE + "CPU:     ", Fore.WHITE + get_cpu_info()['brand_raw'], Style.RESET_ALL)

# Get the current memory usage
memory = psutil.virtual_memory()
ram_bar = "/" * int(memory.percent / 2) + " " * (50 - int(memory.percent / 2))
ram_gb = round(memory.total / (1024 ** 3), 2)
print(Fore.BLUE + "lllllll lllllll      ",     "RAM:     ",      Fore.WHITE + "[{}]".format(ram_bar), Style.RESET_ALL)

# Get the disk usage of all disks
for disk in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(disk.mountpoint)
        percent_used = round(usage.used / usage.total * 100)  # round to the nearest integer
        disk_bar = "/" * max(1, int(percent_used / 2)) + " " * (50 - max(1, int(percent_used / 2)))
        disk_gb = round(usage.total / (1024 ** 3), 2)
        print(Fore.BLUE + "lllllll lllllll      ",     "({}):   ".format(disk.device),    Fore.WHITE + "[{}]".format(disk_bar), Style.RESET_ALL)
    except (PermissionError, OSError):
        print("({}):    [Permission Denied]".format(disk.device))