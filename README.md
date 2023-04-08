# AGS Toolbox 🧰
Utility Adventure Game Studio software to help manage, install, and uninstall different AGS Editor versions

For usability information and questions, go to the [**ags forums topic**](https://www.adventuregamestudio.co.uk/forums/index.php?topic=59938.0).

![](https://user-images.githubusercontent.com/2244442/230735148-7aa061f5-90f7-4db7-ab7f-fcb5a5ea243f.png)

_inspired by [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/), but different_

This software is **Windows** only - since AGS Editor is Windows only. This may change in the future - compatibility is kept with macOS and Linux, but functionality may be absent.


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

***WARNING⚠:*** if you are using Python from Windows Store, most writes to `AppData/Local` and similar [will be redirected](https://github.com/python/cpython/issues/95029) and you will not be able to properly use or debug AGS Toolbox, I recomend you use a Win32 Python to avoid debugging frustrations.

There's probably ways to break the redirection from MS Windows Store Python, but we need to look carefully to not break cross os compatibility, so we may need to diverge Windows vs Nix, see https://github.com/python/cpython/issues/85368
