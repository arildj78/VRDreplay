import prefs
from getAllMedia import GetAllMedia
from event import GetUniqueEvents
from prefs import MarkerColor

import ctypes  # An included library with Python install.
def Mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

class MboxStyle:
    Ok = 0
    OkCancel = 1
    AbortRetryIgnore = 2
    YesNoCancel = 3
    YesNo = 4
    RetryCancel = 5
    CancelTryagainContinue = 6





import os
import sys
import datetime
from glob import glob
from argparse import ArgumentParser
import readTag
from fixMkvDuration import fixMkvDuration
from fixTagWrongStartTime import fixTagWrongStartTime
from timeline import Timeline
# settings

# *******************************
# GLOBAL VARIABLES
# *******************************

presetName = "Default" # You have to define this preset by your self. <----

markerColor = "Yellow"

timelines : list[Timeline]
timelines = []

# customization point

def modifyProject(proj):
    """
    This function is called with created project.
    media: Project
    """
    # first thing first. set preset of the project
    result = proj.SetPreset("Debrief")
    if not result:
        print("You should create a Project Setting Preset named 'Debrief'")
    else:
        print("Debrief loaded")

    a = proj.SetSetting('videoMonitorFormat', 'HD 1080p 25')
    b = proj.SetSetting('videoDeckFormat', 'HD 1080p 25')   #TODO This setter is broken in DaVinci Resolve 18.1 Build 16
    c = proj.SetSetting('timelineFrameRate', '25')
    d = proj.SetSetting('timelinePlaybackFrameRate', '25')  #TODO This setter is broken in DaVinci Resolve 18.1 Build 16
    e = proj.SetSetting('perfOptimisedMediaOn', '0')
    f = proj.SetSetting('perfProxyMediaMode', '0')




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

def createNewTimeline(mediaPool, name, unixStartTime:int):
        dtStartTime = datetime.datetime.utcfromtimestamp(unixStartTime)

        startTimecode = dtStartTime.strftime('%H:%M:%S') + ':00'

        timeline = mediaPool.CreateEmptyTimeline(name)
        #result = timeline.SetSetting("useCustomSettings", "1")
        #if not result:
        #   print("Unable to set custom settings")
        #result = timeline.SetSetting("timelineFrameRate", "25")
        #if not result:
        #   print("Unable to set framerate")

        timeline.SetStartTimecode(startTimecode)
        
        #Add the required number of tracks
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")


        #Set the names of tracks
        timeline.SetTrackName("video", prefs.EO_ACT_TRACK[0], prefs.EO_ACT_TRACK[1])
        timeline.SetTrackName("video", prefs.EO_OPP_TRACK[0], prefs.EO_OPP_TRACK[1])
        timeline.SetTrackName("video", prefs.MCC_TRACK[0], prefs.MCC_TRACK[1])
        timeline.SetTrackName("video", prefs.QUAD_TRACK[0], prefs.QUAD_TRACK[1])
        
        timeline.SetTrackName("audio",prefs.PILOT_TRACK[0], prefs.PILOT_TRACK[1])
        timeline.SetTrackName("audio",prefs.COPILOT_TRACK[0], prefs.COPILOT_TRACK[1])
        timeline.SetTrackName("audio",prefs.SO_TRACK[0], prefs.SO_TRACK[1])
        timeline.SetTrackName("audio",prefs.FE_TRACK[0], prefs.FE_TRACK[1])

        
        #Set the visibility of tracks.
        timeline.SetTrackEnable("video", prefs.EO_ACT_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.EO_OPP_TRACK[0], False)
        timeline.SetTrackEnable("video", prefs.MCC_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.QUAD_TRACK[0], True)

        timeline.SetTrackEnable("audio", prefs.PILOT_TRACK[0], True)
        timeline.SetTrackEnable("audio", prefs.COPILOT_TRACK[0], False)
        timeline.SetTrackEnable("audio", prefs.SO_TRACK[0], False)
        timeline.SetTrackEnable("audio", prefs.FE_TRACK[0], False)

        return timeline


def LockAllTracks(timeline):
        #Set the all tracks to locked
        a = timeline.SetTrackLock("video", prefs.EO_ACT_TRACK[0], True)
        b = timeline.SetTrackLock("video", prefs.EO_OPP_TRACK[0], True)
        c = timeline.SetTrackLock("video", prefs.MCC_TRACK[0], True)
        d = timeline.SetTrackLock("video", prefs.QUAD_TRACK[0], True)

        e = timeline.SetTrackLock("audio", prefs.PILOT_TRACK[0], True)
        f = timeline.SetTrackLock("audio", prefs.COPILOT_TRACK[0], True)
        g = timeline.SetTrackLock("audio", prefs.SO_TRACK[0], True)
        h = timeline.SetTrackLock("audio", prefs.FE_TRACK[0], True)


def createProject(memo=None):
    today = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
    name = prefs.PROJECT_NAME_PREFIX + today
    if memo:
        name += '-%s' % memo
    
    proj = projectManager.CreateProject(name)
    if proj:
        modifyProject(proj)
        


        allMedia = GetAllMedia()
        uniqueEvents = GetUniqueEvents()
        fixMkvDuration(allMedia)
        fixTagWrongStartTime(allMedia)

        mediaPool = proj.GetMediaPool()





        i=0                      #Progress used for debugging
        print("Starting import") #Progress used for debugging
        import time              #Instrumentation
        t0 = time.perf_counter() #Instrumentation
        
        
        subClips: list[readTag.SubClip]
        
        timeLineCounter = 0
        timeLineStartFrame = 0
        
        for media in allMedia:

            if media.startOfTimeline:
                timeLineCounter = timeLineCounter + 1
                
                dtStartTime : datetime.datetime
                dtStartTime = datetime.datetime.utcfromtimestamp(media.startTime)
                timeLineStartFrame = 25 * (dtStartTime.hour * 3600 +
                                           dtStartTime.minute * 60 +
                                           dtStartTime.second) 
                name = dtStartTime.strftime("%Y-%m-%d %H:%M:%S")

                
                print(f'Media.startTime{media.startTime}')
                print(f'tl.startTime{media.subClips[0].StartSec}')

                tl = Timeline(createNewTimeline(mediaPool, name, media.startTime))
                #tl.startTime = media.subClips[0].StartSec  # Replaced for debugging. startTime was set to the time of the second subclip
                tl.startTime = media.startTime
                #tl.endTime = media.subClips[-1].EndSec
                tl.name = name

                proj.SetCurrentTimeline(tl.timeline)
                timelines.append(tl)
            
            timelines[timeLineCounter-1].endTime = media.stopTime #Update end of current timeline with the latest mediafile
            
            medieaPoolItem = mediaStorage.AddItemListToMediaPool(media.mediaFile)


            #if media.trackType == prefs.TrackType.VIDEO:
            print("Filename".ljust(53) + '\t' + "trackIndex" + '\t' + "Timeline start" + '\t' + "startFrame" + '\t' + "endFrame" + '\t' + "frameCount" + '\t' + "Timeline end")
            print("----------------------------------------------------------------------------------------------------------------------------------------------------")
            for subClip in media.subClips:
                newClip = {
                    "mediaPoolItem" : medieaPoolItem[0],                                 #The media file to be inserted
                    "trackIndex" : media.trackNumber,                                    #Track to insert the media in
                    "startFrame" : subClip.startFrame,                                   #The first frame in the media to be used
                    "endFrame" : subClip.endFrame,                                       #The last frame in the media to be used
                    "recordFrame" : subClip.clipFirstFrame + subClip.recordFrameFirst,   #The timeline location (in frames) to insert the clip at
                    "recordFrameEnd" :  subClip.clipFirstFrame + subClip.recordFrameLast #For debugging. The last frame on the timeline occupied by the clip
                }
                print(media.tagFile + '\t' +
                        str(newClip["trackIndex"]).ljust(10) + '\t' + 
                        str(newClip["recordFrame"]).ljust(14) + '\t' + 
                        str(newClip["startFrame"]).ljust(10) + '\t' + 
                        str(newClip["endFrame"]).ljust(8) + '\t' + 
                        str(subClip.frameCount).ljust(10) + '\t' +
                        str(newClip["recordFrameEnd"]).ljust(12))
                mediaPool.AppendToTimeline( [newClip] )
            print()
            print()
        
        for tl in timelines:
            print(tl)
            proj.SetCurrentTimeline(tl.timeline)
            for event in uniqueEvents:
                print(f'Event: {event.time}')
                if tl.coversTimestamp(event.time):
                    frameID = tl.TimestampToFrameID(event.time)
                    print(f'Event: {event}')
                    print(f'frameID: {frameID}')
                    print('-----------')
                    tl.timeline.AddMarker(frameID, MarkerColor.YELLOW, "Event", "", 1)
            res = LockAllTracks(tl.timeline)
            

        t1 = time.perf_counter()  #Instrumentation
        print("Import complete")  #Progress used for debugging
        duration = t1-t0          #Instrumentation
        print("The import took %.1f seconds" % duration) #Instrumentation
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
resolve.LoadLayoutPreset('Debrief')

Mbox("Import VRD", "The import is complete", MboxStyle.Ok)

sys.exit()
