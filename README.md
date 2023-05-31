# VRDreplay
Script for DaVinci Resolve to import and sync audio and video from the 101

## Prerequisite
Version tested in parenthesis
* DaVinci Resolve Studio (18.1 build 16)
* Python (3.10.10)
* [PyUSB](https://github.com/pyusb/pyusb)
* [libusb-package](https://github.com/pyocd/libusb-package)
* Create a UI Layout named **Debrief** in Resolve

## Installation
* Clone or copy the script to the folder
`C:\Users\username\AppData\Roaming\Blackmagic Design\DaVinci Resolve\Support\Fusion\Scripts\Comp\VRDreplay`
* Change DaVinci Resolve setting `DaVinci Resolve -> Preferences... -> General -> System -> External scripting using` to `Local` or `Network`
* Create a Windows shortcut to **python.exe "C:\\..\\Import_VRD.py"** with icon set to Helicopter.ico

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
* [Undocumented Resolve API functions - (trackIndex and recordFrame)](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=113040)


# The media files
## General information
Both the video and audio media files are stored as .mkv files with an accompanying .tag file with identical root file names. The .mkv file holds the media while the .tag file holds timing information on each frame to be used when syncing for playback.

## MKV
The [Matroska file format](https://www.matroska.org/technical/elements.html). Note that the byte order is BIG ENDIAN. 

## TAG
The video .tag files contain data as shown in the table below, while the .tag files accompanying the audio only has frame, unix time and nanoseconds, no additional data.

| Line no | Text       | Description                                      | Decode               |
|---------|------------|--------------------------------------------------|----------------------|
| 39166   | 62.759998  | Frame at second                                  | 62.76                |
| 39167   | 1661781846 | [Unix timestamp](https://www.unixtimestamp.com)  | Aug 29 2022 14:04:06 |
| 39168   | 919834895  | Nanoseconds to be added to timestamp             | 0.919834895 sec      |
| 39169   | 7          | Lines of additional data                         |                      |
| 39170   | 3008       | Unknown data 1                                   |                      |
| 39171   | 3008       | Unknown data 2                                   |                      |
| 39172   | 3012       | Unknown data 3                                   |                      |
| 39173   | 3012       | Unknown data 4                                   |                      |
| 39174   | 3008       | Unknown data 5                                   |                      |
| 39175   | 2952       | Unknown data 6                                   |                      |
| 39176   | 924        | Unknown data 7                                   |                      |


# Problems with the .mkv files
There seems to be multiple problems with the .mkv video files. The following are beeing investigated.
* Duration is one frame to short
* Missing frames

## Duration
*Segment information -> Duration (tag 0x4489)* is one frame to short. Typically each video file is 7500 frames but duration is set to 7499. The duration is given in ticks as a double and seems to be 1ms per tick. The exact value for ticks can be found in *Segment information -> Timestamp scale (tag 0x2AD7B1)* and is given in nanoseconds per tick. This script will assume 1ms pr tick and increase the duration of every file with 40ms to reveal the lost frame at the end of the clip.

| No of frames | No of ticks | Hex tag  | Double as hex            |
|--------------|-------------|----------|--------------------------|
| 7501         | 300 040     | 44 89 88 | 41 12 50 20 00 00 00 00  |
| 7502         | 300 080     | 44 89 88 | 41 12 50 C0 00 00 00 00  |

## Missing frames
The files seems to be of variable framerate close to 25 fps resulting in approximately 40ms pr frame. However, multiple frames in each clip are less than 0.05ms resulting in missing frames in DaVinci Resolve. This script handles this problem by assuming 25fps and cutting each file in multiple subclips based on the timings given in the .tag file effectively removing the missing frames.

