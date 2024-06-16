import prefs
from getAllMedia import GetAllMedia
from event import GetUniqueEvents, CreateEventMarkerClip, InsertEventMarkerClip
from timeofday import CreateTimeOfDayClip
from prefs import MarkerColor
import daVinciConnection

import ctypes  # An included library with Python install.
import win32gui
import win32com.client

from tqdm import tqdm

DAVINCI_WINDOWTEXT = 'DaVinci Resolve'

class WindowHandles:
    def __init__(self, windowText) -> None:
        self.windowText = windowText
        self.hWindows = []
        self.foundHandle = False
        self.numberOfHandles = 0

    def EnumWindows_callback(self, hwnd, lParam):
        windowText = win32gui.GetWindowText(hwnd)
        if self.windowText in windowText:
            self.hWindows.append(hwnd)
            self.foundHandle = True
            self.numberOfHandles = self.numberOfHandles + 1




def Mbox(title, text, style):
    daVinciWindows = WindowHandles(DAVINCI_WINDOWTEXT)
    
    win32gui.EnumWindows(daVinciWindows.EnumWindows_callback, None)
    hWnd = daVinciWindows.hWindows[0] #If multiple daVinci windows, use the first. TODO - Handle this better. TODO - Handle hWnd.len() = 0

    shell = win32com.client.Dispatch("WScript.Shell")
    shell.SendKeys('%') #Send left Alt key to let Windows change the foreground window. Failure to send the Alt makes SetForegroundWindow fail if another app is on top.

    win32gui.SetForegroundWindow(hWnd)

    return ctypes.windll.user32.MessageBoxW(hWnd, text, title, style)

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
from fixMkv import fixMkv
from fixTagWrongStartTime import fixTagWrongStartTime
from timeline import Timeline
# settings

# *******************************
# GLOBAL VARIABLES
# *******************************

presetName = "Default" # You have to define this preset by your self. <----

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
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("video")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")
        timeline.AddTrack("audio", "stereo")


        #Set the names of tracks
        timeline.SetTrackName("video", prefs.EVENT_MARKER_TRACK[0], prefs.EVENT_MARKER_TRACK[1])
        timeline.SetTrackName("video", prefs.TIME_TRACK[0], prefs.TIME_TRACK[1])
        timeline.SetTrackName("video", prefs.RMCAM_TRACK[0], prefs.RMCAM_TRACK[1])
        timeline.SetTrackName("video", prefs.DOCCAM_TRACK[0], prefs.DOCCAM_TRACK[1])
        timeline.SetTrackName("video", prefs.SOFECAM_TRACK[0], prefs.SOFECAM_TRACK[1])
        timeline.SetTrackName("video", prefs.TAIL_TRACK[0], prefs.TAIL_TRACK[1])
        timeline.SetTrackName("video", prefs.MCC_TRACK[0], prefs.MCC_TRACK[1])
        timeline.SetTrackName("video", prefs.OPLS_TRACK[0], prefs.OPLS_TRACK[1])
        timeline.SetTrackName("video", prefs.HOISTCAM_TRACK[0], prefs.HOISTCAM_TRACK[1])
        timeline.SetTrackName("video", prefs.EO_ACT_TRACK[0], prefs.EO_ACT_TRACK[1])
        timeline.SetTrackName("video", prefs.EO_OPP_TRACK[0], prefs.EO_OPP_TRACK[1])
        timeline.SetTrackName("video", prefs.QUAD_TRACK[0], prefs.QUAD_TRACK[1])
        
        timeline.SetTrackName("audio",prefs.PILOT_TRACK[0], prefs.PILOT_TRACK[1])
        timeline.SetTrackName("audio",prefs.COPILOT_TRACK[0], prefs.COPILOT_TRACK[1])
        timeline.SetTrackName("audio",prefs.SO_TRACK[0], prefs.SO_TRACK[1])
        timeline.SetTrackName("audio",prefs.FE_TRACK[0], prefs.FE_TRACK[1])
        timeline.SetTrackName("audio",prefs.SOFECAM_AUDIO_TRACK[0], prefs.SOFECAM_AUDIO_TRACK[1])
        timeline.SetTrackName("audio",prefs.DOCCAM_AUDIO_TRACK[0], prefs.DOCCAM_AUDIO_TRACK[1])
        timeline.SetTrackName("audio",prefs.RMCAM_AUDIO_TRACK[0], prefs.RMCAM_AUDIO_TRACK[1])

        
        #Set the visibility of tracks.
        timeline.SetTrackEnable("video", prefs.EVENT_MARKER_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.TIME_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.RMCAM_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.DOCCAM_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.SOFECAM_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.TAIL_TRACK[0], False)
        timeline.SetTrackEnable("video", prefs.MCC_TRACK[0], False)
        timeline.SetTrackEnable("video", prefs.OPLS_TRACK[0], False)
        timeline.SetTrackEnable("video", prefs.HOISTCAM_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.EO_ACT_TRACK[0], True)
        timeline.SetTrackEnable("video", prefs.EO_OPP_TRACK[0], False)
        timeline.SetTrackEnable("video", prefs.QUAD_TRACK[0], False)

        timeline.SetTrackEnable("audio", prefs.PILOT_TRACK[0], True)
        timeline.SetTrackEnable("audio", prefs.COPILOT_TRACK[0], False)
        timeline.SetTrackEnable("audio", prefs.SO_TRACK[0], False)
        timeline.SetTrackEnable("audio", prefs.FE_TRACK[0], False)
        timeline.SetTrackEnable("audio", prefs.SOFECAM_AUDIO_TRACK[0], False)
        timeline.SetTrackEnable("audio", prefs.DOCCAM_AUDIO_TRACK[0], False)
        timeline.SetTrackEnable("audio", prefs.RMCAM_AUDIO_TRACK[0], False)

        return timeline


def LockAllTracks(timeline):
        #Set the all tracks to locked
        timeline.SetTrackLock("video", prefs.EVENT_MARKER_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.TIME_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.TAIL_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.OPLS_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.HOISTCAM_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.EO_ACT_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.EO_OPP_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.MCC_TRACK[0], True)
        timeline.SetTrackLock("video", prefs.QUAD_TRACK[0], True)

        timeline.SetTrackLock("audio", prefs.PILOT_TRACK[0], True)
        timeline.SetTrackLock("audio", prefs.COPILOT_TRACK[0], True)
        timeline.SetTrackLock("audio", prefs.SO_TRACK[0], True)
        timeline.SetTrackLock("audio", prefs.FE_TRACK[0], True)


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
        fixMkv(allMedia)
        fixTagWrongStartTime(allMedia)

        mediaPool = proj.GetMediaPool()
        root_folder = mediaPool.GetRootFolder()
        rawMaterial_folder = mediaPool.AddSubFolder(root_folder, 'Raw material')
        composite_folder =  mediaPool.AddSubFolder(root_folder, 'Composite')
        video_folder = mediaPool.AddSubFolder(rawMaterial_folder, 'Video')
        audio_folder = mediaPool.AddSubFolder(rawMaterial_folder, 'Audio')
        graphics_folder = mediaPool.AddSubFolder(rawMaterial_folder, 'Graphics')

        i=0                      #Progress used for debugging
        print("Starting import") #Progress used for debugging
        import time              #Instrumentation
        t0 = time.perf_counter() #Instrumentation
        
        
        subClips: list[readTag.SubClip]
        
        timeLineCounter = 0
        timeLineStartFrame = 0
        
        for media in tqdm(allMedia): #tqdm creates a progress bar while iterating through allMedia



            if media.startOfTimeline:
                timeLineCounter = timeLineCounter + 1
                
                dtStartTime : datetime.datetime
                dtStartTime = datetime.datetime.utcfromtimestamp(media.startTime)
                timeLineStartFrame = 25 * (dtStartTime.hour * 3600 +
                                           dtStartTime.minute * 60 +
                                           dtStartTime.second) 
                name = dtStartTime.strftime("%Y-%m-%d %H:%M:%S")

                
                #print(f'Media.startTime{media.startTime}')
                #print(f'tl.startTime{media.subClips[0].StartSec}')

                mediaPool.SetCurrentFolder(root_folder)
                
                tl = Timeline(createNewTimeline(mediaPool, name, media.startTime), mediaPool)
                #tl.startTime = media.subClips[0].StartSec  # Replaced for debugging. startTime was set to the time of the second subclip
                tl.startTime = media.startTime
                #tl.endTime = media.subClips[-1].EndSec
                tl.name = name

                proj.SetCurrentTimeline(tl.timeline)
                timelines.append(tl)
            
            timelines[timeLineCounter-1].endTime = media.stopTime #Update end of current timeline with the latest mediafile
            


            if media.trackType == prefs.TrackType.VIDEO :
                mediaPool.SetCurrentFolder(video_folder)
            if media.trackType == prefs.TrackType.AUDIO :
                mediaPool.SetCurrentFolder(audio_folder)

            tryAgain = True
            tryAgainCounter = 0
            while tryAgainCounter < 10 and tryAgain: 
                medieaPoolItem = mediaStorage.AddItemListToMediaPool(media.mediaFile)
                if medieaPoolItem == []:
    
                    tryAgain = True
                    tryAgainCounter = tryAgainCounter + 1
                    #print(f'{tryAgainCounter} retries to import file: {media.mediaFile}')
                else:
                    tryAgain = False
            
            if tryAgain:
                #tryAgain has not been reset meaning that the tryAgainCounter has expired and this file is abandoned
                print(f'Unable to import file after {tryAgainCounter} attempts: {media.mediaFile}')
                continue # Move on to the next file in allMedia
            

            #if media.trackType == prefs.TrackType.VIDEO:
            #print("Filename".ljust(53) + '\t' + "trackIndex" + '\t' + "Timeline start" + '\t' + "startFrame" + '\t' + "endFrame" + '\t' + "frameCount" + '\t' + "Timeline end")
            #print("----------------------------------------------------------------------------------------------------------------------------------------------------")


            for subClip in media.subClips:
                newClip = {
                    "mediaPoolItem" : medieaPoolItem[0],                                 #The media file to be inserted
                    "trackIndex" : media.trackNumber,                                    #Track to insert the media in              e.g. 4
                    "startFrame" : subClip.startFrame,                                   #The first frame in the media to be used   e.g. 6002
                    "endFrame" : subClip.endFrame,                                       #The last frame in the media to be used    e.g. 7501
                    "recordFrame" : subClip.clipFirstFrame + subClip.recordFrameFirst,   #The timeline location (in frames) to insert the clip at       e.g. 1 239 324 + 6000
                    "recordFrameEnd" :  subClip.clipFirstFrame + subClip.recordFrameLast #For debugging. The last frame on the timeline occupied by the clip
                }
                mediaPool.AppendToTimeline( [newClip] )

        
        mediaPool.SetCurrentFolder(graphics_folder)
        markerClip = CreateEventMarkerClip(proj)
        

        mediaPool.SetCurrentFolder(composite_folder)
        for tl in timelines:
            #print(tl)
            proj.SetCurrentTimeline(tl.timeline)

            #Join all video clips in each video track to a new compound clip
            quadtrack_items = tl.timeline.GetItemListInTrack(prefs.TrackType.VIDEO,  prefs.QUAD_TRACK[0])
            mcc_items       = tl.timeline.GetItemListInTrack(prefs.TrackType.VIDEO,  prefs.MCC_TRACK[0])
            eo_opp_items    = tl.timeline.GetItemListInTrack(prefs.TrackType.VIDEO,  prefs.EO_OPP_TRACK[0])
            eo_act_items    = tl.timeline.GetItemListInTrack(prefs.TrackType.VIDEO,  prefs.EO_ACT_TRACK[0])
            quadtrack_clip_info = {"name" : prefs.QUAD_TRACK[1]   + '_' + tl.name}
            mcc_clip_info       = {"name" : prefs.MCC_TRACK[1]    + '_' + tl.name}
            eo_opp_clip_info    = {"name" : prefs.EO_OPP_TRACK[1] + '_' + tl.name}
            eo_act_clip_info    = {"name" : prefs.EO_ACT_TRACK[1] + '_' + tl.name}
            quad_compound = tl.timeline.CreateCompoundClip(quadtrack_items, quadtrack_clip_info)
            tl.timeline.CreateCompoundClip(mcc_items, mcc_clip_info)
            tl.timeline.CreateCompoundClip(eo_opp_items, eo_opp_clip_info)
            tl.timeline.CreateCompoundClip(eo_act_items, eo_act_clip_info)

            #Prepare quad data for duplication into separate tracks
            quad_start_frame = quad_compound.GetStart()
            quad_mediapool_item = quad_compound.GetMediaPoolItem()
            
            #Add Hoist cam track (duplicate of quad, cropped and scaled)
            hoist_clip = {
                    "mediaPoolItem" : quad_mediapool_item,     #The media file to be inserted
                    "trackIndex" : prefs.HOISTCAM_TRACK[0],    #Track to insert the media in              e.g. 4
                    "recordFrame" : quad_start_frame           #The timeline location (in frames) to insert the clip at       e.g. 1 239 324 + 6000
                    }
            hoist_timelineitem = mediaPool.AppendToTimeline( [hoist_clip] )
            hoist_timelineitem[0].SetProperty({'Pan': -287.0,         'Tilt': -1079.0,
                                               'ZoomX': 0.65,        'ZoomY': 0.65,
                                               'AnchorPointX': -673.0, 'AnchorPointY': 540.0,
                                               'RotationAngle': 90.0,
                                               'CropLeft': 256.0,
                                               'CropRight': 1012.0,
                                               'CropTop': 0.0,
                                               'CropBottom': 548.0}
                                               )

            
            #Add OPLS track (duplicate of quad, cropped and scaled)
            opls_clip = {
                    "mediaPoolItem" : quad_mediapool_item,     #The media file to be inserted
                    "trackIndex" : prefs.OPLS_TRACK[0],        #Track to insert the media in              e.g. 4
                    "recordFrame" : quad_start_frame           #The timeline location (in frames) to insert the clip at       e.g. 1 239 324 + 6000
                    }
            opls_timelineitem = mediaPool.AppendToTimeline( [opls_clip] )            
            opls_timelineitem[0].SetProperty({'Pan': -1122.0,           'Tilt': 324.0,
                                              'ZoomX': 0.690,        'ZoomY': 0.690,
                                              'AnchorPointX': 334.0, 'AnchorPointY': -258.0,
                                              'RotationAngle': 0.0,
                                              'CropLeft': 1083.0,
                                              'CropRight': 409.0,
                                              'CropTop': 537.0,
                                              'CropBottom': 9.0,
                                              'CompositeMode': resolve.COMPOSITE_SCREEN }
                                              )


            #Add Tail track (duplicate of quad, cropped and scaled)
            tail_clip = {
                    "mediaPoolItem" : quad_mediapool_item,     #The media file to be inserted
                    "trackIndex" : prefs.TAIL_TRACK[0],        #Track to insert the media in              e.g. 4
                    "recordFrame" : quad_start_frame           #The timeline location (in frames) to insert the clip at       e.g. 1 239 324 + 6000
                    }
            tail_timelineitem = mediaPool.AppendToTimeline( [tail_clip] )            
            tail_timelineitem[0].SetProperty({'Pan': -256.0,           'Tilt': 535.0,
                                              'ZoomX': 0.535,        'ZoomY': 0.535,
                                              'AnchorPointX': -704.0, 'AnchorPointY': 4.0,
                                              'RotationAngle': 0.0,
                                              'CropLeft': 257.0,
                                              'CropRight': 1012.0,
                                              'CropTop': 537.0,
                                              'CropBottom': 12.0 }
                                              )

            #Add time of day on Time Track
            tod_mediaPool_item = CreateTimeOfDayClip(proj)
            tod_clip = {
                    "mediaPoolItem" : tod_mediaPool_item,     #The media file to be inserted
                    "trackIndex" : prefs.TIME_TRACK[0],        #Track to insert the media in              e.g. 4
                    "recordFrame" : quad_start_frame,           #The timeline location (in frames) to insert the clip at       e.g. 1 239 324 + 6000
                    "recordFrameEnd" :  quad_start_frame + 180000 #For debugging. The last frame on the timeline occupied by the clip
                    }
            tod_timelineitem = mediaPool.AppendToTimeline( [tod_clip] )            



            #Join all audio clips in each video track to a new compound clip
            pilot_items   = tl.timeline.GetItemListInTrack(prefs.TrackType.AUDIO,  prefs.PILOT_TRACK[0])
            copilot_items = tl.timeline.GetItemListInTrack(prefs.TrackType.AUDIO,  prefs.COPILOT_TRACK[0])
            so_items      = tl.timeline.GetItemListInTrack(prefs.TrackType.AUDIO,  prefs.SO_TRACK[0])
            fe_items      = tl.timeline.GetItemListInTrack(prefs.TrackType.AUDIO,  prefs.FE_TRACK[0])
            pilot_clip_info   = {"name" : prefs.PILOT_TRACK[1]   + '_' + tl.name}
            copilot_clip_info = {"name" : prefs.COPILOT_TRACK[1] + '_' + tl.name}
            so_clip_info      = {"name" : prefs.SO_TRACK[1]      + '_' + tl.name}
            fe_clip_info      = {"name" : prefs.FE_TRACK[1]      + '_' + tl.name}
            tl.timeline.CreateCompoundClip(pilot_items, pilot_clip_info)
            tl.timeline.CreateCompoundClip(copilot_items, copilot_clip_info)
            tl.timeline.CreateCompoundClip(so_items, so_clip_info)
            tl.timeline.CreateCompoundClip(fe_items, fe_clip_info)



            for event in uniqueEvents:
                #print(f'Event: {event.time}')
                if tl.coversTimestamp(event.time):
                    frameID = tl.TimestampToFrameID(event.time)
                    tl.timeline.AddMarker(frameID, MarkerColor.YELLOW, "Event", "", 1)
                    InsertEventMarkerClip(tl, markerClip, prefs.EVENT_MARKER_TRACK[0], event.time, 75)                    
            res = LockAllTracks(tl.timeline)



        mediaPool.SetCurrentFolder(root_folder)

        t1 = time.perf_counter()  #Instrumentation
        print("Import complete")  #Progress used for debugging
        duration = t1-t0          #Instrumentation
        print("The import took %.1f seconds" % duration) #Instrumentation
    return proj





resolve, projectManager, currentProject, mediaStorage, fusion = daVinciConnection.initConnection()




projectManager.CloseProject(projectManager.GetCurrentProject())
createProject()
resolve.OpenPage("edit")
resolve.LoadLayoutPreset('Debrief')

Mbox("Import VRD", "The import is complete", MboxStyle.Ok)

sys.exit()
