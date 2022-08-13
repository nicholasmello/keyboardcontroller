# Keyboard Controller
This repo contains a command line program as well as a GUI

## Required Setup
The [Tuxedo Keyboard](https://github.com/tuxedocomputers/tuxedo-keyboard) Kernel module must be installed before either tool in this repo can be used.

To add the .desktop file copy it to a location where you system will recognize it (such as ~/.local/share/applications) and copy keyctl to /usr/bin/

## Command Line
```
usage: keyctl [-h] [-c color] [-b brightness] [-g]
  -h, --help     show this help message and exit
  -c color       color of the keyboard (0xFFFFFF)
  -b brightness  brightness of the keyboard (0xFF)
  -g             get current value
```

The program can be installed with the command 

`mv ./keyctl /usr/bin/`

## QT GUI
The GUI uses the toolbar with the included keyboard icon so it will always be available when you want to make a change

## Operating System
These programs have only been tested on my computer which is running KDE Neon