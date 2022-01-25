# AGS Toolbox 🧰
Utility software to help manage, install, and uninstall different AGS Editor versions

_inspired by [JetBrains Toolbox](https://www.jetbrains.com/toolbox-app/), but different_


⚠**under construction**⚠

This software is Windows only - since the Editor is Windows only. This will allow to develop a more tailor made software. This may change in the future.


## Building a portable EXE

Install pyinstaller (`pip install pyinstaller`) and then use it on a `cmd.exe` prompt

    pyinstaller agstoolbox.spec
	
This should generate a `agstoolbox.exe` file under the `dist/` directory in the project root.

##  Desired features

- Download any archive.zip of any AGS version from 3.5.0 forward
- buttons for launching Editor or opening folder in windows explorer
- monitoring new releases
- check download integrity with some hashing
- allow setting a default AGS to use
- allow removing a downloaded Editor from hard drive
- launching link to online AGS manual, and forums
- detect AGS editors installed through other means (but not manage them)
- see how much storage each AGS Editor is using.
- add folders as project libraries (may contain `game.agf` files)
- allow listing game projects in libraries, with version used in `game.agf`
- allow opening a game project directory in the file explorer


## how it (will!) works

A [NotifyIcon](https://docs.microsoft.com/en-us/dotnet/desktop/winforms/controls/app-icons-to-the-taskbar-with-wf-notifyicon?view=netframeworkdesktop-4.8) is placed on the taskbar. This allows the application to continuously run and occasionally check for new releases (at launch, once each six hours?).
The icon has two options, open the toolbox, and quit. If toolbox is opened a small panel is loaded.
- This panel contains a clearly highlighted AGS Editor marked as default (it's possible no default is set), and a list of found AGS Editors. 
- A settings gear icon is available, as is two links, one for the online manual and one for the forums. 
- AGS Editors that are managed by the toolbox have the option to go to load and tree dots for doing additional things (like going to it's folder). 
- AGS Editors that are not managed by the toolbox are available to launch but marked not as such. 
- The list is ordered by the most recent version to least. 
- Pre-releases (alpha and beta versions) are marked as such in their icons.
- If a newer release is available, an icon is placed to allow quick download of it.

In the settings following options are available
- you can filter release versions you are not interested (say 3.5.1.X)
