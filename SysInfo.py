import os
import platform
import psutil
import math
from screeninfo import get_monitors
from cpuinfo import get_cpu_info
import datetime
from colorama import Fore, Style
from itertools import zip_longest
from requests import get

__version__ = "0.0.3"

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

pub_ip = get("https://api.ipify.org").text
pub_ip_info = "Pub IP:  {}{}{}".format(Fore.WHITE, pub_ip, Style.RESET_ALL)


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

if platform.system() == "Windows":
    os_logo = "\n".join([
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
    os_color_start = Fore.BLUE
    os_color_end = Fore.BLUE
elif platform.system() == "Arch":
    os_logo = "\n".join([
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
    os_color_start = Fore.BLUE
    os_color_end = Fore.BLUE
elif platform.system() == "Apple":
    os_logo = "\n".join([
        Fore.GREEN +  "               (     ",
        Fore.GREEN +  "           ((((      ",
        Fore.GREEN +  "           (((       ",
        Fore.GREEN +  "   ((((((((((((((((( ",
        Fore.YELLOW + "  (((((((((((((((((  ",
        Fore.YELLOW + " /////////////////   ",
        Fore.RED +    " /////////////////   ",
        Fore.MAGENTA + " ((((((((((((((((((( ",
        Fore.BLUE +   "  (((((((((((((((((((",
        Fore.BLUE +   "    (((((((((((((((  ",
        ])
    os_color_start = Fore.GREEN
    os_color_end = Fore.BLUE
else:
    os_logo = "\n".join([
        Fore.RED + "                ///  ",
        Fore.RED + "              ///    ",
        Fore.RED + "            ///      ",
        Fore.RED + "          ///        ",
        Fore.RED + "        ///          ",
        Fore.RED + "      ///            ",
        Fore.RED + "    ///              ",
        Fore.RED + "  ///                ",
        Fore.RED + "///                  ",
    ])
    os_color_start = Fore.RED
    os_color_end = Fore.RED

part2 = "\n".join([
    os_info,
    uptime_info,
    screen_info,
    cpu_info,
    pub_ip_info,
    ram_info,
] + disk_info)

# Calculate Spacing
if part2.count("\n") - os_logo.count("\n") <= 1:
    spacing_top_rows = part2.count("\n") - os_logo.count("\n")
    spacing_bottom_rows = 0
else:
    # Use math.ceil for even distribution of extra rows
    spacing_top_rows = math.ceil((part2.count("\n") - os_logo.count("\n")) / 2)
    spacing_bottom_rows = math.floor((part2.count("\n") - os_logo.count("\n")) / 2)  

# Create Spacing Strings
spacing_top = os_color_start + "                "  # Simplified spacing string
spacing_bottom = os_color_end + "                " 

# Construct part1
part1 = "\n".join([
    *(spacing_top for _ in range(spacing_top_rows)),  # Use unpacking (*)
    os_logo,
    *(spacing_bottom for _ in range(spacing_bottom_rows)) 
])



# Print in two columns
for line1, line2 in zip_longest(part1.split("\n"), part2.split("\n"), fillvalue=''):
    print("{:<40} {:<40}".format(line1, line2))
print(Style.RESET_ALL)
Fore.RESET

