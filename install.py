import os
import subprocess
import shutil
import sys
import re


alias = "SysInfo"
# Ask the user if they want to install Sysinfo
user_input = input("Do you want to install Sysinfo including all necessary libraries? (y/n): ")

# Check if the user wants to install Sysinfo
if user_input.lower() == 'y':
    print("Installing Sysinfo...")

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

    # Check if the PowerShell profile exists
    profile_check = subprocess.run(['powershell', '-Command', 'Test-Path $PROFILE'], capture_output=True, text=True)
    if 'True' in profile_check.stdout:
        # Check if the alias already exists in the profile
        alias_check = subprocess.run(['powershell', '-Command', f'if (Get-Command {alias} -ErrorAction SilentlyContinue) {{ "True" }} else {{ "False" }}'], capture_output=True, text=True)
        if 'True' in alias_check.stdout:
            print("Alias already exists.")
        else:
            command = f'Add-Content -Path $PROFILE -Value "`nfunction {alias} {{ python {script_path} }}"'
            subprocess.run(['powershell', '-Command', command], check=True)
            print("Alias added to existing profile.")
    else:
        # If the profile doesn't exist, ask the user if they want to create it
        user_input = input("A PowerShell profile does not exist. Do you want to create one? (y/n): ")
        if user_input.lower() == 'y':
            subprocess.run(['powershell', '-Command', 'New-Item -path $PROFILE -type file -force'], check=True)
            command = f'Add-Content -Path $PROFILE -Value "`nfunction {alias} {{ python {script_path} }}"'
            subprocess.run(['powershell', '-Command', command], check=True)
            print("Profile created and alias added.")
        else:
            print("Quitting installation...")
            sys.exit(0)


    # List of necessary libraries
    libraries = ['psutil', 'screeninfo', 'py-cpuinfo', 'colorama']

    # Install the necessary libraries
    for library in libraries:
        subprocess.run([sys.executable, '-m', 'pip', 'install', library])

    # Copy the SystemInfo.py script to the folder
    shutil.copy(script_path, os.path.join(folder_path, 'SysInfo.py'))

    # Update the script path to the new location
    script_path = os.path.join(folder_path, 'SysInfo.py')
    
    # Print the success message
    print("Sysinfo has been installed successfully!")

    # Check if the user wants to restart the terminal
    print("Please restart your terminal for the changes to take effect.")
else:
    print("Quitting installation...")
    sys.exit(0)
