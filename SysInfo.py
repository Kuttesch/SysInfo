import os
import platform
import psutil
from screeninfo import get_monitors
from cpuinfo import get_cpu_info
import datetime
from colorama import Fore, Style
from itertools import zip_longest

__version__ = "0.0.1"

# Check the operating system
os_info = "OS:      {}{}".format(Fore.WHITE, platform.system())

# Get the OS uptime
boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
uptime = datetime.datetime.now() - boot_time

days = uptime.days
hours, remainder = divmod(uptime.seconds, 3600)
minutes, _ = divmod(remainder, 60)

uptime_info = "Uptime:  {}{} days, {} hours, {} minutes{}".format(Fore.WHITE, days, hours, minutes, Style.RESET_ALL)

# Get the screen resolution
primary_monitor = get_monitors()[0]
screen_info = "Screen:  {}{}*{}{}".format(Fore.WHITE, primary_monitor.width, primary_monitor.height, Style.RESET_ALL)

# Get the CPU information
cpu_info = "CPU:     {}{}".format(Fore.WHITE, get_cpu_info()['brand_raw'])

# Get the current memory usage
memory = psutil.virtual_memory()
ram_bar = "/" * int(memory.percent / 2) + " " * (50 - int(memory.percent / 2))
ram_gb = round(memory.total / (1024 ** 3), 2)
ram_info = "RAM:     {}[{}]{}".format(Fore.WHITE, ram_bar, Style.RESET_ALL)

# Get the disk usage of all disks
disk_info = []
for disk in psutil.disk_partitions():
    try:
        usage = psutil.disk_usage(disk.mountpoint)
        percent_used = round(usage.used / usage.total * 100)
        disk_bar = "/" * max(1, int(percent_used / 2)) + " " * (50 - max(1, int(percent_used / 2)))
        disk_gb = round(usage.total / (1024 ** 3), 2)
        disk_info.append("({}):   {}[{}]{}".format(disk.device, Fore.WHITE, disk_bar, Style.RESET_ALL))
    except (PermissionError, OSError):
        disk_info.append("({}):    [Permission Denied]".format(disk.device))

# Part 1
# if os_info == "Apple":
    part1 = "\n".join([
        Fore.BLUE + "llllllllll llllllllll",
        Fore.BLUE + "llllllllll llllllllll",
        Fore.BLUE + "llllllllll llllllllll",
        Fore.BLUE + "llllllllll llllllllll",
        Fore.BLUE + "                     ",
        Fore.BLUE + "llllllllll llllllllll",
        Fore.BLUE + "llllllllll llllllllll",
        Fore.BLUE + "llllllllll llllllllll",
        Fore.BLUE + "llllllllll llllllllll",
    ])
""" elif os_info == "Arch":
    part1 = "\n".join([
        Fore.BLUE + "                     ",
        Fore.BLUE + "          ll         ",
        Fore.BLUE + "         llll        ",
        Fore.BLUE + "        l llll       ",
        Fore.BLUE + "       lllllllll     ",
        Fore.BLUE + "     lllll  lllll    ",
        Fore.BLUE + "    lllll    lllll   ",
        Fore.BLUE + "   llllll    llllll  ",
        Fore.BLUE + " ll                ll",
        ])
elif os_info == "Windows":
    part1 = "\n".join([
        Fore.WHITE +  "               (     ",
        Fore.GREEN +  "           ((((      ",
        Fore.GREEN +  "           (((       ",
        Fore.GREEN +  "   ((((((((((((((((( ",
        Fore.RED +    " ,,,,,,,,,,,,,,,,,,  ",
        Fore.RED +    " /////////////////   ",
        Fore.RED +    " /////////////////   ",
        Fore.RED +    " ((((((((((((((((((( ",
        Fore.BLUE +   "  (((((((((((((((((((",
        Fore.BLUE +   "    (((((((((((((((  ",
        ])
"""
part2 = "\n".join([
    os_info,
    uptime_info,
    screen_info,
    cpu_info,
    ram_info,
] + disk_info)

# Print in two columns
for line1, line2 in zip_longest(part1.split("\n"), part2.split("\n"), fillvalue=''):
    print("{:<40} {:<40}".format(line1, line2))
print(Style.RESET_ALL)
Fore.RESET

