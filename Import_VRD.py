# import os
# import sys
# import datetime
# from glob import glob
# from argparse import ArgumentParser

# # settings

# projectNamePrefix = "vrd-"
# presetName = "Default" # You have to define this preset by your self. <----
# mediaDirectories = [
#     r"G:\Vlog\ZV1-64GB-1", # Change these directories to your locations. <----
#     r"G:\Vlog\GoPro Black 7",
#     r"G:\Vlog\WebCam HD",
#     r"G:\Vlog\Captured Screen",
# ]
# mediaExtensions = [
#     "mkv", # in lowercase
#     #"mp4",
#     #"mov",
# ]
# markerColor = "Yellow"






# import DaVinciResolveScript as dvr_script




# TESTFILE = "C:/Windows/SystemResources/Windows.UI.SettingsAppThreshold/SystemSettings/Assets/SDRSample.mkv"


# resolve = dvr_script.scriptapp("Resolve")
# fusion = resolve.Fusion()
# projectManager = resolve.GetProjectManager()
# #projectManager.CreateProject("Hello World")


# project = projectManager.GetCurrentProject()
# mediapool = project.GetMediaPool()




import prefs
from getAllMedia import GetAllMedia

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)










import os
import sys
import datetime
from glob import glob
from argparse import ArgumentParser

# settings

presetName = "Default" # You have to define this preset by your self. <----
# mediaDirectories = [
#     "G:\\", # Change these directories to your locations. <----
#     #r"G:\VRD Dump\2023-02-16 0264", # Change these directories to your locations. <----
#     #r"G:\VRD Dump\2023-02-16 0264\vrd_database\MCC\MCC_0000\MCC_0000_000",
#     # r"G:\Vlog\WebCam HD",
#     # r"G:\Vlog\Captured Screen",
# ]
# mediaExtensions = [
#     "mkv", # in lowercase
#     "mp4", 
#     "mov",
# ]
markerColor = "Yellow"

# customization point

def modifyProject(proj):
    """
    This function is called with created project.
    media: Project
    """
    # first thing first. set preset of the project
    #proj.SetPreset(presetName)


def modifyMedia(media):
    """
    This function is called with each media added to media pool.
    media: MediaPoolItem
    """
    # props = media.GetClipProperty()
    # print(props)
    pass

def modifyClip(clip):
    """
    This function is called with each media added to timeline.
    It is a good chance to set clip color, set LUT.
    media: TimelineItem
    """
    pass
    #clip.SetLUT(1, os.path.join(RESOLVE_LUT_DIR, r"Sony SLog2 to Rec709.ilut"))

#define paths for Resolve components

RESOLVE_SUPPORT_DIR = os.path.join(*[
    os.environ["PROGRAMDATA"],
    "Blackmagic Design",
    "DaVinci Resolve",
    "Support",
])

RESOLVE_LUT_DIR = os.path.join(*[
    RESOLVE_SUPPORT_DIR,
    "LUT",
])

RESOLVE_SCRIPT_API = os.path.join(*[
    RESOLVE_SUPPORT_DIR,
    "Developer",
    "Scripting",
])

RESOLVE_SCRIPT_LIB = os.path.join(*[
    os.environ["ProgramFiles"],
    "Blackmagic Design",
    "DaVinci Resolve",
    "fusionscript.dll",
])

# actions

def createProject(memo=None):
    today = datetime.date.today().isoformat()
    name = prefs.PROJECT_NAME_PREFIX + str(today)
    if memo:
        name += '-%s' % memo

    proj = projectManager.CreateProject(name)
    if proj:
        #modifyProject(proj)

        proj.SetSetting('videoMonitorFormat', 'HD 1080p 25')
        proj.SetSetting('videoDeckFormat', 'HD 1080p 25')
        proj.SetSetting('timelineFrameRate', 25.0)
        proj.SetSetting('timelinePlaybackFrameRate', '25')

        proj.SetSetting('perfOptimisedMediaOn', 0)
        proj.SetSetting('perfProxyMediaMode', 0)


        allMedia = GetAllMedia()

        # mediaList = []
        # for media in allMedia:
        #     mediaList.append(media.mediaFile)

        # mediaStorage.AddItemListToMediaPool(mediaList) 


        # for item in mediaList:
        #     print(item)


        i=0
        import time
        print("Starting import")
        t0 = time.perf_counter()
        #mediaList_In_MediaPool = mediaStorage.AddItemListToMediaPool(mediaList)
        for media in allMedia:
            i = i+1
            print(i)
            mediaStorage.AddItemListToMediaPool(media.mediaFile)

        t1 = time.perf_counter()
        print("Import complete")
        duration = t1-t0
        print("The import took %.1f seconds" % duration)







        mediaPool = proj.GetMediaPool()
        
        timeline = mediaPool.CreateEmptyTimeline("test")
        result = timeline.SetSetting("useCustomSettings", "1")
        if not result:
            print("Unable to set custom settings")
        result = timeline.SetSetting("timelineFrameRate", "25")
        if not result:
            print("Unable to set framerate")

        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")

        timeline.SetTrackName("video", prefs.MCC_TRACK[0], prefs.MCC_TRACK[1])
        timeline.SetTrackName("video", prefs.EO_OPP_TRACK[0], prefs.EO_OPP_TRACK[1])
        timeline.SetTrackName("video", prefs.EO_ACT_TRACK[0], prefs.EO_ACT_TRACK[1])
        timeline.SetTrackName("video", prefs.QUAD_TRACK[0], prefs.QUAD_TRACK[1])
        
        timeline.SetTrackName("audio",1,"Pilot")
        timeline.SetTrackName("audio",2,"2P")
        timeline.SetTrackName("audio",3,"SO")
        timeline.SetTrackName("audio",4,"FE")









        # for media in mediaList:
            
        #     for m in mediaList:
        #         #print(m.GetMediaId())
        #         pass

        #     # for media in mediaList:
        #     #     modifyMedia(media)

        #     # pos = timeline.GetEndFrame() - timeline.GetStartFrame()
        #     # timeline.AddMarker(pos, markerColor, path, "", 1)

        #     # mediaPool.AppendToTimeline(mediaList)

        #     # clips = timeline.GetItemListInTrack('video', 1)
        #     # if clips:
        #     #     clipStart = clipCount
        #     #     clipCount += len(mediaList)

        #     #     for clip in clips[clipStart:clipCount]:
        #     #         modifyClip(clip)


        #     newClip = {
        #         "mediaPoolItem" : media,
        #         "startFrame" : 1500,
        #         "endFrame" : 2500,
        #         "trackIndex" : 1,
        #         "recordFrame" : 90000,
        #     }
        #     a = mediaPool.AppendToTimeline( [newClip] )

        #     newClip = {
        #         "mediaPoolItem" : mediaList[2],
        #         "startFrame" : 3500,
        #         "endFrame" : 4500,
        #         "trackIndex" : 2,
        #         "recordFrame" : 90025,
        #     }
        #     b = mediaPool.AppendToTimeline( [newClip] )


        #     newClip = {
        #         "mediaPoolItem" : mediaList[2],
        #         "startFrame" : 500,
        #         "endFrame" : 1000,
        #         "trackIndex" : 4,
        #         "recordFrame" : 90250,
        #     }
        #     mediaPool.AppendToTimeline( [newClip] )      

        #     a=timeline.GetItemListInTrack("video",3)
        #     print(a[0].GetName()) 

    return proj








# define environment variables

os.environ["RESOLVE_SCRIPT_API"] = RESOLVE_SCRIPT_API
os.environ["RESOLVE_SCRIPT_LIB"] = RESOLVE_SCRIPT_LIB

# setup python path

sys.path.append(os.path.join(RESOLVE_SCRIPT_API, 'Modules'))

# now it's ready to import module
import DaVinciResolveScript as dvrs

# major objects
resolve = dvrs.scriptapp("Resolve")
if not resolve:
    print("Please launch DaVinci Resolve first.")
    sys.exit()

resolve.OpenPage("deliver")
projectManager = resolve.GetProjectManager()
mediaStorage = resolve.GetMediaStorage()
fusion = resolve.Fusion()

# command line options

parser = ArgumentParser(description="Create DaVinci Resolve project and import media files")
parser.add_argument("-d", "--date", dest="dates", action="append", help="Default is today. Multiple date is okay.")
parser.add_argument("--verbose", action="store_const", const=True, default=False)
parser.add_argument("memo", nargs='?', default="")

args = parser.parse_args()

verbose = args.verbose

projectManager.CloseProject(projectManager.GetCurrentProject())
createProject(memo=args.memo)
resolve.OpenPage("edit")

sys.exit()
