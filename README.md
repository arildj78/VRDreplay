# VRDreplay
Script for DaVinci Resolve to import and sync audio and video from the 101

## Prerequisite
Version tested in parenthesis
* DaVinci Resolve Studio (18.1 build 16)
* Python (3.10.10) and (3.11.1)(3.13.2)
* pip install pywin32 (for å gi win32gui)
* Create a Project setting named **Debrief** in Resolve
* Create a UI Layout named **Debrief** in Resolve

## Installation
* Clone or copy the script to the folder
`C:\VRDreplay`
* Change DaVinci Resolve setting `DaVinci Resolve -> Preferences... -> General -> System -> External scripting using` to `Local` or `Network`
* On the Windows desktop, create a Windows shortcut to **python.exe "C:\\..\\Import_VRD.py"** with icon set to Helicopter.ico

### Windows environment variables set to
* PYTHONPATH = C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\Modules
*  RESOLVE_SCRIPT_API = C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting
*  RESOLVE_SCRIPT_LIB = C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll

## Description
The script is available through the helicopter shortcut created on the desktop. Invoking the script will automatically locate the VRD disk connected to the USB adapter and create a new project with a timeline containing all the recordings. If there is a significant period without recordings (multiple sorties) additional timelines will be created.

## Programming reference
While writing this script, the following references have been used (not an exhaustive list)
* [Unofficial DaVinci Resolve Scripting Documentation](https://deric.github.io/DaVinciResolve-API-Docs/)
* [ResolveDevDoc’s documentation](https://resolvedevdoc.readthedocs.io/en/latest/index.html)
* C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting\README.txt
* [basuke/create-vlog-project.py](https://gist.github.com/basuke/908ed2b0f41d9d995f7955d3cebfb9ae)
* [Info on how to set timeline framerate](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=150093)
* [Undocumented Resolve API functions - (trackIndex and recordFrame)](https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=113040)
* [Looking up Timeline item properties](https://gist.github.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8)


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

## EVT
The event files holds a timestamp for when the event switch has been toggled in the cockpit or by the SO. It also holds additional information that still is not fully reversed. See the document [Reversing the Event file](fileformats/evt.md) for details.


# Problems with the .mkv files
There seems to be multiple problems with the .mkv video files. The following are beeing investigated.
* Duration is one frame to short
* For files in the Recovered_Segments folder, the file header is missing segment size
* Missing frames
* Codec issue during playback
* QUAD video has a timing issue

## Duration
*Segment information -> Duration (element ID 0x4489)* is one frame too short. Typically each video file is 7500 frames but duration is set to 7499. The duration is given in ticks as a double and seems to be 1ms per tick. The exact value for ticks can be found in *Segment information -> Timestamp scale (element ID 0x2AD7B1)* and is given in nanoseconds per tick. This script will assume 1ms pr tick and increase the duration of every file with 40ms to reveal the lost frame at the end of the clip.

| No of frames | No of ticks | Element ID  | Size Length | Length | Double as hex            |
|--------------|-------------|-------------|-------------|--------|--------------------------|
| 7501         | 300 040     | 44 89       |           8 | 8      | 41 12 50 20 00 00 00 00  |
| 7502         | 300 080     | 44 89       |           8 | 8      | 41 12 50 C0 00 00 00 00  |

If the recording has ended abnormally, the file will likely be in a folder named `Recovered_Segments` without Duration `ID 0x4489` set correctly. In offset `0x160` you will rather find a void space of 11 bytes: `EC 01 00 00 00 00 00 00 02 00 00`. The fix for this is the same as above but we also need to write the Element ID `0x4489` as well as element size `0x88` followed by the 8 bytes of duration.

Both of these duration related problems are handled by the fixMkv module.

## Missing segment size
It seems that video files in the Recoverd_Segments folder has segment size set to `01 FF FF FF FF FF FF FF` (unknown). fixMkv will change this to the size of the remainder of the file.

| Offset | Element ID  | Size Length  | Size                  |
|--------|-------------|--------------|-----------------------|
| 0x2F   | 18 53 80 67 | 01=(7 bytes) | FF FF FF FF FF FF FF  |
| 0x2F   | 18 53 80 67 | 01=(7 bytes) | File size - 59 bytes *|

*) Offset 0x2F + 4 bytes Element ID + 8 bytes length descriptor = 59 bytes

## Missing frames
The files seems to be of variable framerate close to 25 fps resulting in approximately 40ms pr frame. However, multiple frames in each clip are less than 0.05ms resulting in missing frames in DaVinci Resolve. This script handles this problem by assuming 25fps and cutting each file in multiple subclips based on the timings given in the .tag file effectively removing the missing frames.

## Codec issue during playback
The following has been observed when playing back the video files

| Software               | Version            | Observation                                                                                                              |
|------------------------|--------------------|--------------------------------------------------------------------------------------------------------------------------|
| Windows 11 photo app   | 2023.11050.16005.0 | Plays video with no noticeable problems.                                                                                 |
| VLC                    | 3.0.18             | Garbled image on lower half of the video. ***SOLVED*** by disabling hardware acceleration in settings                    |
| DaVinci Resolve (Free) | 18.1.4             | The missing frame is rendered as a red banner with the text **Media Offline**, the following frames are rendered correct |
| DaVinci Resolve Studio | 18.1.4             | The missing frame is rendered as a solid grey frame, the following 5 frames are rendered grey with small artifacts       |

## QUAD video has a timing issue
Occasionally the quad video has a timing issue. It seems like the video is split into the normal 7500 frames per file but instead of the normal 5 minutes it contains 6 minutes of material, resulting in 20.83 frames per second. When edited in a video editor with 25fps the video needs to be slowed down to 83.333%.

It is not known if the problem is always exactly 6 minutes of video in a 5 minute file or if the timing differs between sorties. Normally though, the quad video is exactly 5 minutes with 7500 frames.

In one sortie the problem was exactly 360 seconds per 7500 frames. No problem on the sortie before or after.

By investigating one of the .tag files from that sortie it seems that there are four frames of duration 40ms before one frame of duration 80ms. This patterns seems to be repeating.


## Credit
* [Finding drive letter from VID/PID with C++](https://itecnote.com/tecnote/c-find-and-eject-a-usb-device-based-on-its-vid-pid/)


## References
* [Matroska (MKV) technical specification](https://www.matroska.org/technical/elements.html)
* [EBML specification](https://matroska-org.github.io/libebml/specs.html)
