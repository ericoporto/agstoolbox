# AGS Toolbox 🧰
Utility Adventure Game Studio software to help manage, install, and uninstall different AGS Editor versions

For usability information and questions, go to the [**ags forums topic**](https://www.adventuregamestudio.co.uk/forums/index.php?topic=59938.0).

![](https://user-images.githubusercontent.com/2244442/230735148-7aa061f5-90f7-4db7-ab7f-fcb5a5ea243f.png)

_inspired by [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/), but different_

This software is **Windows** only - since AGS Editor is Windows only. This may change in the future - compatibility is kept with macOS and Linux, but functionality may be absent.


## Installation

You should use the `agstoolbox.exe` from latest release. Place it in a directory under your user like `C:\Users\MY_USER\software\agstoolbox.exe` and double click it.

### Installing from pip

You can install it from [pip](https://pypi.org/project/agstoolbox/)

    pip install agstoolbox

**NOTE:** On MS Windows, instalation from pip may not work correctly, see [Warning on Windows Store Python](#warning-on-windows-store-python) for more information.

## Command Line usage

NOTE: On Windows, due to OS and PyInstaller limitations, `agstoolbox.exe` doesn't work with command line arguments, so `atbx.exe` is made available to for command line arguments.

```sh
$ atbx --help
usage: atbx [-h] [-s {bash,zsh,tcsh}] [-v] {list,install,open,settings} ...

agstoolbox is an application to help manage AGS Editor versions.

positional arguments:
  {list,install,open,settings}
                        command
    list                lists things
    install             install tools
    open                open an editor or project
    settings            modify or show settings

optional arguments:
  -h, --help            show this help message and exit
  -s {bash,zsh,tcsh}    print shell completion script
  -v, --version         get software version.

Copyright 2023 Erico Vieira Porto, MIT.
```

As an example, a command line to force install the latest 3.6 AGS Editor, as a managed Editor is as follows

```sh
$ atbx install editor 3.6 -f
Will install managed AGS Editor release 3.6.0.47
 Downloading... 40475597/40475597 B |████████████████████████████████| AGS-3.6.0.47.zip
Extracting...
Installed release 3.6.0.47
```

### atbx with bash completion on Windows Git-Bash

Check if you have a `~/.bashrc` file, attempt to show it

```sh
cat ~/.bashrc
```

If you get an error message, you don't have one yet, lets generate one

```
cat  /etc/bash.bashrc > ~/.bashrc
```

We are going to create a directory to store additional bash completion in your Windows user home,
and then use atbx to generate the bash completion script and then add a line to bashrc to load it
once a new shell loads.

```
mkdir ~/bash_completion.d/
atbx -s bash > ~/bash_completion.d/atbx
echo "source ~/bash_completion.d/atbx" >> ~/.bashrc
```

Once you close and reload the terminal, using atbx and pressing tab should show the commands, like
`list`, `install`, ...


## Development

### Building a portable EXE

Install pyinstaller (`pip install pyinstaller`) and then use it on a `cmd.exe` prompt

    pyinstaller agstoolbox.spec
	
This should generate a `agstoolbox.exe` file under the `dist/` directory in the project root.

### Coding

[PyCharm Community](https://www.jetbrains.com/pycharm/) is highly recommended for development, you can setup a venv and have it install dependencies and running the project as soon as you point to the root directory.
Be sure to set agstoolbox as the command to run in it.

This project uses Python 3, I am currently developing with 3.9, because it provides compatibility with additional type information that is not supported out of the box in previous versions. 

Use pip to install dependencies

    pip install -r requirements.txt

For running, you can call the script on the rootfolder directly.

    python agstoolbox

    
## Warning on Windows Store Python

If you are using Python from Windows Store, most writes to `AppData/Local` and similar [will be redirected](https://github.com/python/cpython/issues/95029) and you will not be able to properly use or debug AGS Toolbox, I recomend you use a **Win32** Python to avoid debugging frustrations.

There's probably ways to break the redirection from MS Windows Store Python, but we need to look carefully to not break cross os compatibility, so we may need to diverge Windows vs Nix, see https://github.com/python/cpython/issues/85368


## Author and License

This code is made by Érico Porto, and licensed with MIT [`LICENSE`](LICENSE).
