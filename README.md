# VRDreplay
Script for DaVinci Resolve to import and sync audio and video from the 101

## Prerequisite
Version tested in parenthesis
* DaVinci Resolve Studio (18.1 build 16)
* Python (3.10.10)
* PyUSB

## Installation
* Clone or copy the script to the folder
`C:\Users\username\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Comp\VRDreplay`
* Change DaVinci Resolve setting `DaVinci Resolve -> Preferences... -> General -> System -> External scripting using` to `Local` or `Network`

### Windows environment variables set to
* PYTHONPATH = C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules
*  RESOLVE_SCRIPT_API = C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting
*  RESOLVE_SCRIPT_LIB = C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll

## Description
The script is available through the menu `Workspace -> Scripts -> Comp -> VRDreplay -> Import_VRD`. Invoking the script will automatically locate the VRD disk connected to the USB adapter and create a new project with a timeline containing all the recordings. If there is a significant period without recordings (multiple sorties) additional timelines will be created.

## Programming reference
While writing this script, the following references have been used (not an exhaustive list)
* [Unofficial DaVinci Resolve Scripting Documentation](https://deric.github.io/DaVinciResolve-API-Docs/)
* [ResolveDevDoc’s documentation](https://resolvedevdoc.readthedocs.io/en/latest/index.html)
* C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt
* [basuke/create-vlog-project.py](https://gist.github.com/basuke/908ed2b0f41d9d995f7955d3cebfb9ae)
* [Info on how to set timeline framerate](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=150093)
* [Discussion on placing clips on specific place in timeline (trackIndex and recordFrame)](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=113040)