# AGS Toolbox 🧰
Utility Adventure Game Studio software to help manage, install, and uninstall different AGS Editor versions

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/agstoolbox) ![PyPI](https://img.shields.io/pypi/v/agstoolbox) ![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/ericoporto/agstoolbox?color=blue&label=%F0%9F%93%85)

For usability information and questions, go to the [**ags forums topic**](https://www.adventuregamestudio.co.uk/forums/index.php?topic=59938.0).

![](https://user-images.githubusercontent.com/2244442/230735148-7aa061f5-90f7-4db7-ab7f-fcb5a5ea243f.png)

_inspired by [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/), but different_

This software is **Windows** only - since AGS Editor is Windows only. This may change in the future - compatibility is kept with macOS and Linux, but functionality may be absent.


## Installation

You should use the `agstoolbox.exe` from latest release. Place it in a directory under your user like `C:\Users\MY_USER\software\agstoolbox.exe` and double click it.

### Installing from pip

You can install it from [pip](https://pypi.org/project/agstoolbox/)

    pip install agstoolbox

**NOTE:** On MS Windows, installation from pip may not work correctly, see [Warning on Windows Store Python](#warning-on-windows-store-python) for more information.

## Command Line usage

NOTE: On Windows, due to OS and PyInstaller limitations, `agstoolbox.exe` doesn't work with command line arguments, so `atbx.exe` is made available to for command line arguments.

```sh
$ atbx --help
usage: atbx [-h] [-s {bash,zsh,tcsh}] [-v] {list,install,open,build,settings,export,pack} ...

agstoolbox is an application to help manage AGS Editor versions.

positional arguments:
  {list,install,open,build,settings,export}
                        command
    list                lists things
    install             install tools
    open                open an editor or project
    build               builds an ags project
    settings            modify or show settings
    export              export from ags project
    pack                package build results

optional arguments:
  -h, --help            show this help message and exit
  -s {bash,zsh,tcsh}    print shell completion script
  -v, --version         get software version.

Copyright 2026 Erico Vieira Porto, MIT.
```

As an example, a command line to force install the latest 3.6 AGS Editor, as a managed Editor is as follows

```sh
$ atbx install editor 3.6 -f
Will install managed AGS Editor release 3.6.0.47
 Downloading... 40475597/40475597 B |████████████████████████████████| AGS-3.6.0.47.zip
Extracting...
Installed release 3.6.0.47
```

Additionally, when using `--version` to check the version, atbx will attempt to alert if a newer version is available online.

---

### Commands

- [`list`](#command-list)
  - [`list editors`](#command-list-editors)
  - [`list projects`](#command-list-projects)
- [`install`](#command-install)
  - [`install editor`](#command-install-editor)
- [`open`](#command-open)
  - [`open editor`](#command-open-editor)
  - [`open project`](#command-open-project)
- [`build`](#command-build)
- [`settings`](#command-settings)
  - [`settings show`](#command-settings-show)
  - [`settings set`](#command-settings-set)
- [`export`](#command-export)
  - [`export script`](#command-export-script)
  - [`export template`](#command-export-template)
- [`pack`](#command-pack)

#### Command: list

This command has two required subcommands, you must call with either for it to work.

##### Command: list editors

This is meant to list the available AGS Editors. It will use the agstoolbox settings behind the scenes, and by default will only list managed editors.
It supports the options below:

- `-u, --unmanaged`, search for unmanaged editors, following the directories specified in settings.
- `-d, --download`, it will list editors available for download (from AGS GitHub releases).
- `-p PATH, --path PATH`, it will instead look for AGS Editors in a specific path, ignoring settings.

Example:

```
atbx list editors -d
```

Will return a list of editors, with their versions and their links.

##### Command: list projects

This command is for retrieving a list of AGS Game projects, it will by default search the directories configured in settings.
It supports one option below:
- `-p PATH, --path PATH`, it will instead look for AGS Game Projects in the specified path, ignoring settings.

Example:

```
atbx list projects -p .
```

Will instead list any available AGS Game Project in the current directory or any subdirectory, recursively.

---

#### Command: install

This command is meant for installing tools, for now only AGS Editor is available, but you still have to specify it with its subcommand.

##### Command: install editor

This command will download the AGS Editor zip archive and unpack in the managed editors directory.
It requires an argument that has to be either a version (e.g.: 4.0.0.25) or you can pass the directory of an AGS Game Project, and it will pick the specific version that project was last saved with.
It supports the options below:
- `-f, --force`, if the editor is already in the managed editors, it will be redownloaded if necessary, and it will unpack overwriting it in the managed editors directory.
- `-q, --quiet`, it won't print the download progress, this may be useful in a CI environment.

Example:

```
atbx install editor 3.6.3.3
```

This will install editor 3.6.3.3 and make it available as a managed editor.

---

#### Command: open

This command requires a subcommand, see below.

##### Command: open editor

This command is meant to open a specific editor version, which you need to pass as an argument. If it can't find an exact match it will warn and try to find one compatible to the specified version.

Example:

```
atbx open editor 3.6.3.3
```

##### Command: open project

This command requires an AGS Game Project path as an argument. It will try to find an Editor compatible with the project and open it.
By default, this command will block the terminal - you can `Ctrl+C` in the terminal to force close AGS Editor, or it will proceed normally when the Editor exits.
It supports the options below:
- `-e VER, --editor VER`, force specific version of AGS Editor instead of project default
- `-n, --non-blocking`, if you use this, the command line will return and the Editor will not block it while it's open.
- `-w, --which-editor`, don't actually open the editor with the project, instead return the path of the Editor that was matched for the project.

Example:

```
atbx open project -n .
```

Opens the AGS Game Project in the current directory with the matching editor, without blocking the terminal.

---

#### Command: build

This command requires an AGS Game Project path as an argument.

In case of an error, this command returns non-zero exit code, so it's safe to use it in CI pipelines.

It will open the matched AGS Editor (the same from `open project` command), but it will use the `/compile` AGS Editor parameter to for it to build the project and exit.
It supports the options below:
- `-e VER, --editor VER`, force specific version of AGS Editor instead of project default
- `-n, --non-blocking`, if you use this, the command line will return and the Editor will not block it while it's open. Don't use this on a CI environment.
- `-t SEC, --timeout SEC`, the seconds to wait before interrupting the build. This only works when blocking. It's useful if a project may cause an exception that somehow leads to unwanted user interaction that can block the build.

Example:

```
atbx build -t 300 .
```

Builds the project in the current directory, but exits if it isn't finished in 5 minutes.

---

#### Command: settings

This command requires a subcommand, see below.

**NOTE:** I haven't had time to proper adjust this, if you need to change settings in your computer the easy way is to use the agstoolbox, the graphical version, it has a proper graphical menu you can configure everything in much easier way.

##### Command: settings show

This will print all the settings in the terminal, so you can quickly read it.

##### Command: settings set

This command can be used to set the value of the settings from the command line. For now only `tools_install_dir` can be passed, along with the dir to install it.

Example:

```
atbx settings set tools_install_dir /MY_TOOLS
```

This will set the tools install dir as `/MY_TOOLS`. For now, prefer operating the settings with the graphical interface. If you have a need for configuring the settings from the command line open an issue so I can prioritize this.

---

#### Command: export

This command requires a subcommand, see below.

##### Command: export script

This is meant to export a script module (`.scm` file).

It requires three positional arguments, in order:

- `PROJECT_PATH`, path to the project with the module
- `MODULE_NAME`, name of the script module
- `OUT_DIR`, where to export the script module

##### Command: export template

This is meant to export a game as a template. In AGS Editor versions where this is not supported as a command line parameter of the Editor itself, AGS ToolBox will use it's own AGS Template export implementation, but in Editor versions where this is supported, it will use the Editor own machinery to do this, if the Editor is installed.

It supports the options below:
- `-f, --force-editor`, force using the AGSEditor `/maketemplate` command if supported
- `-t SEC, --timeout SEC`, the seconds to wait before interrupting editor export.


---

#### Command: pack

This command will create a directory named `Dist` at the root of your game project path, and put any built binaries there packaged for distribution.
Currently it only support Windows, Web and Linux builds.

- For _Windows_ builds it zips the contents of `Compiled/Windows` directory in a file named `GAMENAME_windows.zip`, and puts it in `Dist` directory.
- For _Web_ builds it does the same, it zips the contents of `Compiled/Web` directory in a file named `GAMENAME_web.zip`, and puts it in `Dist` directory.
- For _Linux_ builds it will archive the contents of `Compiled/Linux` directory in a tar file named `GAMENAME_linux.tar.gz`, and adjust the execution bit of the necessary files to make it executable when unpacked on a Linux distro; this tar file is put in the `Dist` directory.

It requires the positional argument below:

- `PROJECT_PATH`, path to the project with the module

Example:

```
atbx pack .
```

It will package any built games from the project in the current directory and put it in the `Dist` directory it creates.

---

### tab completion on Windows Git-Bash

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

Whenever you update atbx, regenerate it's completion script using
```
atbx -s bash > ~/bash_completion.d/atbx
```

## Development

### Building a portable EXE

Install pyinstaller (`pip install pyinstaller`) and then use it on a `cmd.exe` prompt

    pyinstaller agstoolbox.spec

This should generate a `agstoolbox.exe` file under the `dist/` directory in the project root.

### Coding

[PyCharm Community](https://www.jetbrains.com/pycharm/) is highly recommended for development, you can setup a venv and have it install dependencies and running the project as soon as you point to the root directory.
Be sure to set agstoolbox as the command to run in it.

This project uses Python 3, I am currently developing with 3.9, because it provides compatibility with additional type information that is not supported out of the box in previous versions. For now it's been possible to use future imports to keep this type annotation compatible with Python 3.8.

Use pip to install dependencies

    pip install -r requirements.txt

For running, you can call the script on the rootfolder directly.

    python agstoolbox

You can do the same with stbx

    python atbx

You can configure your IDE to run both of these scripts and alternate between them when debugging.


## Warning on Windows Store Python

If you are using Python from Windows Store, most writes to `AppData/Local` and similar [will be redirected](https://github.com/python/cpython/issues/95029) and you will not be able to properly use or debug AGS Toolbox, I recomend you use a **Win32** Python to avoid debugging frustrations.

There's probably ways to break the redirection from MS Windows Store Python, but we need to look carefully to not break cross os compatibility, so we may need to diverge Windows vs Nix, see https://github.com/python/cpython/issues/85368


## Author and License

This code is made by Érico Porto, and licensed with MIT [`LICENSE`](LICENSE).
