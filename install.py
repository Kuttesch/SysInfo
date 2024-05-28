import os
import subprocess
import shutil
import sys
import re

# Ask the user if they want to install Sysinfo
user_input = input("Do you want to install Sysinfo including all necessary libraries? (y/n): ")

# Check if the user wants to install Sysinfo
if user_input.lower() == 'y':
    print("Installing Sysinfo...")

        # Check if the PowerShell profile exists
    profile_check = subprocess.run(['powershell', '-Command', 'Test-Path $PROFILE'], capture_output=True, text=True)

    # If the profile doesn't exist, ask the user if they want to create it
    if 'False' in profile_check.stdout:
        user_input = input("A PowerShell profile does not exist. Do you want to create one? (y/n): ")
        if user_input.lower() == 'y':
            subprocess.run(['powershell', '-Command', 'New-Item -path $PROFILE -type file -force'], check=True)
        else:
            print("Quitting installation...")
            sys.exit(0)

    # Path to the SystemInfo.py script
    script_path = os.path.abspath('SysInfo.py')

    # Ask the user if they want to use the default install path
    user_input = input("Do you want to use the default install path (~/Documents/SysInfo)? If not, please specify your desired path: ")

    # If the user just presses enter, use the default path
    if user_input == '':
        folder_path = os.path.expanduser('~/Documents/SysInfo')
    else:
        # Normalize the path provided by the user
        folder_path = os.path.normpath(user_input)
        # Check if the provided path is a valid path string
        if re.match(r"[<>:\"|?*]", folder_path):
            print("The provided path contains invalid characters. Please try again.")
            sys.exit(1)

    # Create the folder
    os.makedirs(folder_path, exist_ok=True)

     # List of necessary libraries
    libraries = ['psutil', 'screeninfo', 'py-cpuinfo', 'colorama']

    # Install the necessary libraries
    for library in libraries:
        subprocess.run([sys.executable, '-m', 'pip', 'install', library])

    # Copy the SystemInfo.py script to the folder
    shutil.copy(script_path, os.path.join(folder_path, 'SysInfo.py'))

    # Update the script path to the new location
    script_path = os.path.join(folder_path, 'SysInfo.py')

    # PowerShell command to add the alias
    command = f'Add-Content -Path $PROFILE -Value "function SysInfo {{ python {script_path} }}"'

    # Run the command in PowerShell
    subprocess.run(['powershell', '-Command', command], check=True)

    # Print the success message
    print("Sysinfo has been installed successfully!")

    # Check if the user wants to restart the terminal
    print("Please restart your terminal for the changes to take effect.")
else:
    print("Quitting installation...")
    sys.exit(0)