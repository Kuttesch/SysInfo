# SysInfo

SysInfo is a Python project that provides detailed system information. It uses various libraries such as `os`, `platform`, `psutil`, `screeninfo`, `cpuinfo`, `datetime`, `colorama`, and `itertools`.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Known Bugs](#bugs)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install System Information, you need to run the installation script. This script will ask you if you want to install Sysinfo and the necessary libraries. It will also check if the PowerShell profile exists and if not, it will ask you if you want to create one. It will ask you if you want to use the default install path or specify your own. It will then install the necessary libraries, copy the `SystemInfo.py` script to the specified folder, and update the PowerShell profile to add an alias for Sysinfo.

```bash
git clone https://github.com/Kuttesch/SysInfo.git
cd SysInfo
python install.py
```

After running the script, restart your terminal for the changes to take effect.

## Usage

After installation, you can run the script by simply typing `SysInfo` in your terminal.

```bash
SysInfo
```

In this example, the program will start and display detailed system information.

## Bugs

Currently, there are no known bugs. If you find any, please open an issue in the GitHub repository.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)