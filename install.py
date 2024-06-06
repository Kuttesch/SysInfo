import os
import subprocess
import shutil
import sys
import re
import ast


Installer_Path = os.path.abspath('SysInfo.py')

Install_Path_Windows = os.path.expanduser('~/SysInfo')
Install_Path_Linux = os.path.expanduser('~/.local/bin/SysInfo')

libraries = ['psutil', 'screeninfo', 'py-cpuinfo', 'colorama']

alias = "SysInfo"

# Function to get the version number from a Python script
def get_version_number(script_path):
    with open(script_path) as f:
        source_code = f.read()
    module = ast.parse(source_code)
    version_assignments = [node for node in module.body if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name) and node.targets[0].id == '__version__']
    if version_assignments:
        version_number = version_assignments[0].value.s
        print(f"DEBUG: Version number of {script_path} is {version_number}.")
        return version_number
    else:
        return None
        print("DEBUG: Version number of {script_path} not found.")

# Function to check the OS
def osCheck():
    if sys.platform == 'win32':
        return 'Windows'
        print("DEBUG: Windows OS detected.")
    elif sys.platform == 'linux':
        return 'Linux'
        print("DEBUG: Linux OS detected.")
    else:
        return None
        print("DEBUG: Unsupported OS detected.")

# Function to install the required libraries
def libInstall():
    for library in libraries:
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', library], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if 'Requirement already satisfied' in result.stdout:
                print(f"{library} already exists!")
            else:
                print(f"{library} has been installed successfully!")
        except subprocess.CalledProcessError:
            print(f"Failed to install {library}!")

def checkVersion(Install_Path):
    if os.path.exists(Install_Path):
        Installer_Version = get_version_number(Installer_Path)
        Existing_Version = get_version_number(Install_Path + '/SysInfo.py')

        # Compare the version numbers
        if Existing_Version == None or Installer_Version == None or Installer_Version > Existing_Version:
            # Newer version
            return 1
                
        elif Installer_Version < Existing_Version:
            # Older version
            return 2
        else:
            # Same version
            return 3
    else:
        # No version
        return 0

def switchInstall(VersionStatus, OSVersion):
    InstallVersion = "install" + OSVersion + "()"
    if VersionStatus == 0:
        check = input("Do you want to install SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()
    elif VersionStatus == 1:
        print("You have a newer version of SysInfo than the one you're trying to install.")
        check = input("Do you want to downgrade SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()
    elif VersionStatus == 2:
        print("A newer version of SysInfo is available.")
        check = input("Do you want to update SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()
    elif VersionStatus == 3:
        print("You already have the latest version of SysInfo.")
        check = input("Do you want to reinstall SysInfo? (y/n): ")
        if check.lower() == 'y':
            exec(InstallVersion)
        else:
            quitMessage()


def successMessage():
    print("Sysinfo has been installed successfully!")
    print("Please remove the installer directory manually: " + os.path.dirname(Installer_Path))
    print("Please restart your terminal for the changes to take effect.")

def quitMessage():
    print("Quitting installation...")
    sys.exit(0)

# Function to install the SysInfo script
def installWindows():

    print("Installing Sysinfo...")

    # Create the folder
    if os.path.exists(Install_Path_Windows):
        pass
    else:
        os.makedirs(Install_Path_Windows, exist_ok=True)

    # Check if the PowerShell profile exists
    profile_check = subprocess.run(['powershell', '-Command', 'Test-Path $PROFILE'], capture_output=True, text=True)
    if 'True' in profile_check.stdout:
        # Check if the alias already exists in the profile
        alias_check = subprocess.run(['powershell', '-Command', f'if (Get-Command {alias} -ErrorAction SilentlyContinue) {{ "True" }} else {{ "False" }}'], capture_output=True, text=True)
        if 'True' in alias_check.stdout:
            print("Alias already exists.")
        else:
            command = f'Add-Content -Path $PROFILE -Value "`nfunction {alias} {{ python {Install_Path_Windows} }}"'
            subprocess.run(['powershell', '-Command', command], check=True)
            print("DEBUG: Alias added to existing profile.")
    else:
        # If the profile doesn't exist, ask the user if they want to create it
        user_input = input("A PowerShell profile does not exist. Do you want to create one? (y/n): ")
        if user_input.lower() == 'y':
            subprocess.run(['powershell', '-Command', 'New-Item -path $PROFILE -type file -force'], check=True)
            command = f'Add-Content -Path $PROFILE -Value "`nfunction {alias} {{ python {Install_Path_Windows} }}"'
            subprocess.run(['powershell', '-Command', command], check=True)
            print("DEBUG: Profile created and alias added.")
        else:
            print("Quitting installation...")
            sys.exit(0)

    # Install the required libraries
    libInstall()

    # Copy the SystemInfo.py script to the folder
    shutil.copy(Installer_Path, Install_Path_Windows)

    successMessage()

def main():
    os_type = osCheck()
    if os_type == 'Windows':
        VersionStatus = checkVersion(Install_Path_Windows)
        switchInstall(VersionStatus, 'Windows')
    elif os_type == 'Linux':
        checkVersion(Install_Path_Linux)
        switchInstall(VersionStatus, 'Linux')
    else:
        print("Unsupported OS.")
        quitMessage()

