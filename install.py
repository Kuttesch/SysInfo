import os
import subprocess
import shutil

# Path to the SystemInfo.py script
script_path = os.path.abspath('SystemInfo.py')

# Create the folder under Documents
folder_path = os.path.expanduser('~/Documents/SysInfo')
os.makedirs(folder_path, exist_ok=True)

# Copy the SystemInfo.py script to the folder
shutil.copy(script_path, os.path.join(folder_path, 'SystemInfo.py'))

# Update the script path to the new location
script_path = os.path.join(folder_path, 'SystemInfo.py')

# PowerShell command to add the alias
command = f'Add-Content -Path $PROFILE -Value "function SysInfo {{ python {script_path} }}"'

# Run the command in PowerShell
subprocess.run(['powershell', '-Command', command], check=True)

# Instruct the user to restart the terminal
print("Please restart your terminal for the changes to take effect.")