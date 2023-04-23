import prefs
from getAllMedia import GetAllMedia
from readTag import ReadTag
import struct
import os
from mediaClip import MediaClip



def PrintDescription():
    print("********************************************")
    print("    FIX OF .MKV DURATION                    ")
    print("********************************************")
    print("    The .mkv files have a duration          ")
    print("    property that is erroneously set one    ")
    print("    frame too short. This leads to          ")
    print("    a single black frame in the cut         ")
    print("    between the individual media files.     ")
    print("    This script changes the mkv file        ")
    print("    so the last frame is included.          ")
    print("********************************************")
    print("                                            ")
    
    

def ReadMkvDuration(filename:str) -> float:
    with open(filename, "rb") as fileobject:
        fileobject.seek(0x160, os.SEEK_SET)
        tag = fileobject.read(3)
        tag = struct.unpack('BBB', tag)

        if tag != (0x44, 0x89, 0x88):
            raise Exception(prefs.EXCEPTION_MSG_DURATION_ERROR)
            
        duration = fileobject.read(8)
        duration = struct.unpack('>d', duration)

        return duration[0]


def WriteMkvDuration(filename:str, duration:float):
    with open(filename, "r+b") as fileobject:
        fileobject.seek(0x160, os.SEEK_SET)
        tag = fileobject.read(3)
        tag = struct.unpack('BBB', tag)

        if tag != (0x44, 0x89, 0x88):
            raise Exception(prefs.EXCEPTION_MSG_DURATION_ERROR)

        duration = struct.pack('>d', duration)
        fileobject.write(duration)
    

def fixMkvDuration(allMedia:list[MediaClip]):
    DescriptionPrinted = False

    videoFiles = list(filter(lambda x: (x.trackType == prefs.TrackType.VIDEO), allMedia)) #Extract only the videofiles
    videoFiles = sorted(videoFiles, key = lambda x: (x.trackNumber, x.startTime))         #Sort by trackNumber then startTime


    for clip in videoFiles:

        mkvDuration = ReadMkvDuration(clip.mediaFile) 
        endFrame = clip.subClips[-1].endFrame
        tagDuration = float((40 * (endFrame + 1)))

        if  mkvDuration != tagDuration:
            #There is a discrepancy between the duration property in the file and the .tag file.
            #The .mkv file will be patched.                
            
            #Print the patch description on the first run through
            if not DescriptionPrinted:
                PrintDescription()
                DescriptionPrinted = True

            #Apply the patch
            WriteMkvDuration(clip.mediaFile, tagDuration)
            
            #Check if patch was successfully applied
            correctedDuration = ReadMkvDuration(clip.mediaFile)
            if correctedDuration == tagDuration:
                mkvDuration = mkvDuration / 1000               #Change units from milliseconds to seconds
                correctedDuration = correctedDuration / 1000   #Change units from milliseconds to seconds

                mkvDuration = f"{mkvDuration:.3f}"             #Convert to string with three desimal points
                correctedDuration = f"{correctedDuration:.3f}" #Convert to string with three desimal points

                mkvDuration = mkvDuration.rjust(7)             #Right justify by padding with space to 7 characters 
                correctedDuration = correctedDuration.rjust(7) #Right justify by padding with space to 7 characters

                print(f"{clip.mediaFile} :  Successfully changed duration from {mkvDuration} to {correctedDuration} seconds ")
            else:
                print(f"{clip.mediaFile} :  Unable to fix duration of file")

    print()
    print()


if __name__ == "__main__":
    allMedia = GetAllMedia()
    fixMkvDuration(allMedia)
    