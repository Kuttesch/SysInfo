import os
import subprocess
import shutil
import sys
import re
import ast

Install_Path = os.path.expanduser('~/SysInfo/SysInfo.py')
Installer_Path = os.path.abspath('SysInfo.py')

# Function to get the version number from a Python script
def get_version_number(script_path):
    with open(script_path) as f:
        source_code = f.read()
    module = ast.parse(source_code)
    version_assignments = [node for node in module.body if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == '__version__']
    if version_assignments:
        version_number = version_assignments[0].value.s
        return version_number
    else:
        return None


# Function to install the SysInfo script
def install():
    alias = "SysInfo"

    print("Installing Sysinfo...")

    # Create the folder
    os.makedirs(Install_Path, exist_ok=True)

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
            print("DEBUG: Alias added to existing profile.")
    else:
        # If the profile doesn't exist, ask the user if they want to create it
        user_input = input("A PowerShell profile does not exist. Do you want to create one? (y/n): ")
        if user_input.lower() == 'y':
            subprocess.run(['powershell', '-Command', 'New-Item -path $PROFILE -type file -force'], check=True)
            command = f'Add-Content -Path $PROFILE -Value "`nfunction {alias} {{ python {script_path} }}"'
            subprocess.run(['powershell', '-Command', command], check=True)
            print("DEBUG: Profile created and alias added.")
        else:
            print("Quitting installation...")
            sys.exit(0)


    # List of necessary libraries
    libraries = ['psutil', 'screeninfo', 'py-cpuinfo', 'colorama']

    # Install the necessary libraries
    for library in libraries:
        subprocess.run([sys.executable, '-m', 'pip', 'install', library])

    # Copy the SystemInfo.py script to the folder
    shutil.copy(Installer_Path, os.path.join(folder_path, 'SysInfo.py'))


    # Print the success message
    print("Sysinfo has been installed successfully!")

    # Check if the user wants to restart the terminal
    print("Please restart your terminal for the changes to take effect.")


# Check if there's already a version of SysInfo at the target destination
if os.path.exists(Install_Path):
    # Get the version numbers
    Installer_Version = get_version_number(Installer_Path)
    Existing_Version = get_version_number(Install_Path)

    # Compare the version numbers
    if Installer_Version == None or Existing_Version == None:
        check = input("Do you want to install SysInfo? (y/n): ")
        if check.lower() == 'y':
            install()
    else:
        if Installer_Version > Existing_Version:
            print("A newer version of SysInfo is available.")
            check = input("Do you want to update SysInfo? (y/n): ")
            if check.lower() == 'y':
                install()
            else:
                print("Quitting installation...")
                sys.exit(0)
        else:
            print("You already have the latest version of SysInfo.")
            check = input("Do you want to reinstall SysInfo? (y/n): ")
            if check.lower() == 'y':
                install()
            else:
                print("Quitting installation...")
                sys.exit(0)
else:
    check = input("Do you want to install SysInfo? (y/n): ")
    if check.lower() == 'y':
        install()
