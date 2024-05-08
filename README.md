# SysInfo

SysInfo is a Python project that provides detailed system information in the Terminal.

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
Then you will see the following output:

```bash
llllllllll llllllllll               OS:      Windows
llllllllll llllllllll               Uptime:  0 days, 1 hours, 49 minutes
llllllllll llllllllll               Screen:  1920*1200
llllllllll llllllllll               CPU:     AMD Ryzen 5 7530U with Radeon Graphics
                                    RAM:     [///////////////////////////////////////////////   ]
llllllllll llllllllll               (C:\):   [///////////////////////////////////////           ]
llllllllll llllllllll               (D:\):   [////////                                          ]
llllllllll llllllllll               (E:\):   [////////////////////////////////////////          ]
llllllllll llllllllll
```

## Bugs

Currently, there is only a bug that I am aware of. The script does not work on Linux or MacOS. This is because the script uses the `psutil` library, which is not available on Linux or MacOS. I am working on a solution to this problem.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)