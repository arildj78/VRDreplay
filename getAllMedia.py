import os

import re #regEx library

import prefs
from prefs import TrackType

from mediaClip import MediaClip
import reverseRead



#Read start time from start of tag file and stop time from end of taf file
def get_clip_start_stop_time(tagFile:str):
    startTime = 0
    stopTime = 0
    try:
        with open(tagFile, 'r') as fileobject:
            next(fileobject)                   #Skip first line
            startTime  = int(next(fileobject)) #Read line number 2 where the unix time for recording start is stored

            reversedTagFile = reverseRead.reversed_lines(fileobject)                    #Create a generator capable of reading lines from the end of a file
            for lineNo in range(prefs.TAGFILE_LINES_TO_SCAN_FROM_END_TO_FIND_STOPTIME): #If it takes to many attempts to find the timestamp something is wrong
                line = next(reversedTagFile)                                            #Read lines from the end of the .tag file
                value = int(line)            
                if value >= 1e9:                                                        #If the line has a number >= 1e9 it is assumed to be a Epoch Unix Timestamp
                    stopTime = value
                    break

    except:
        startTime = 0
        stopTime = 0
    
    result = (startTime, stopTime)
    return result
    






def GetAllMedia():

    #Initialize an empty list to hold a reference to the media files beeing imported
    mediaFiles = []

    #Create regex objects to identify the files to import
    regex_eo_act = re.compile(prefs.EO_ACT_MKV_FILENAME_REGEX)
    regex_eo_opp = re.compile(prefs.EO_OPP_MKV_FILENAME_REGEX)
    regex_mcc    = re.compile(prefs.MCC_MKV_FILENAME_REGEX)
    regex_quad   = re.compile(prefs.OPLS_XCS_QUAD_MKV_FILENAME_REGEX)


    #Look through all directories and subdirectories for all files and process them
    for dir in prefs.RECORDING_DIRECTORIES:
        for root, dirs, files in os.walk(dir):
            for file in files:
                trackNumber = -1    #If the file beeing processed is a media file, this will get a valid number
                
                #Check if file is a EO Active file
                if regex_eo_act.match(file):
                    trackNumber = prefs.EO_ACT_TRACK[0]
                    trackName = prefs.EO_ACT_TRACK[1]

                #Check if file is a EO Opposite file
                if regex_eo_opp.match(file):
                    trackNumber = prefs.EO_OPP_TRACK[0]
                    trackName = prefs.EO_OPP_TRACK[1]
                
                #Check if file is a MCC file
                if regex_mcc.match(file):
                    trackNumber = prefs.MCC_TRACK[0]
                    trackName = prefs.MCC_TRACK[1]
                
                #Check if file is a Quad file
                if regex_quad.match(file):
                    trackNumber = prefs.QUAD_TRACK[0]
                    trackName = prefs.QUAD_TRACK[1]
                    
                
                #if the file is a mediafile, process it
                if trackNumber >= 0:
                    mkvFile = os.path.join(root, file)
                    tagFile = os.path.splitext(mkvFile)[0] + '.tag'  #From 'c:\myMkvFile.mkv' the string 'c:\myMkvFile.tag' is created
                    
                    if not os.path.isfile(tagFile):
                        tagFile = ''

                    start_stop = get_clip_start_stop_time(tagFile)
                    
                    mc = MediaClip()
                    mc.startTime = start_stop[0]
                    mc.stopTime = start_stop[1]
                    
                    mc.mediaFile = mkvFile
                    mc.tagFile = tagFile
                    mc.trackType = TrackType.VIDEO
                    mc.trackName = trackName
                    mc.trackNumber = trackNumber
                    mediaFiles.append(mc)
                    
                    
                    
    #Sort the clips and assign them to timelines
    mediaFiles.sort()
    previousClip_StopTime = 0
    currentTimeline = -1

    for mediaFile in mediaFiles:
        if mediaFile.startTime > (previousClip_StopTime + prefs.EMPTY_SECONDS_BEFORE_NEW_TIMELINE):
            currentTimeline = currentTimeline + 1
            mediaFile.startOfTimeline = True

        mediaFile.timelineNumber = currentTimeline
        
        previousClip_StopTime = max(previousClip_StopTime, mediaFile.stopTime)

    return mediaFiles





#*********************************************************
#  Check if this is a better way of collecting filenames
#*********************************************************


# def isMediaFile(name):
#     _, ext = os.path.splitext(name)
#     return ext and ext[0] == '.' and ext[1:].lower() in mediaExtensions

# def getMediaFiles(directory):
#     def visit(result, path, names):
#         for name in names:
#             if isMediaFile(name):
#                 result.append(os.path.join(path, name))

#     result = []
#     os.walk(directory, visit, result)
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             result.append(os.path.join(directory, file))
#     return result

# def getMediasOfTheDate(date):
#     pattern = date + "*"

#     for directory in mediaDirectories:
#         for path in glob(os.path.join(directory, pattern)):
#             if os.path.isdir(path):

#                 files = getMediaFiles(path)
#                 if files:
#                     yield (path, files)


if __name__ == "__main__":
    allMedia = GetAllMedia()
    for media in allMedia:
        print(media)