import prefs
from getAllMedia import GetAllMedia
from readTag import ReadTag
import struct
import os
from mediaClip import MediaClip
from tqdm import tqdm



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
        if tag == (0xEC, 0x01, 0x00):
                tag = fileobject.read(8)
                tag = struct.unpack('BBBBBBBB', tag)
                if tag == (0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00):
                    print('Debug - FOUND A RECOVERED SEGMENT with no duration')
                    return -1.0
        
        if tag != (0x44, 0x89, 0x88):
            print(f"Just checked the file: {filename}")
            print(f"The position where duration was expected has the following bytes: {tag}")
            raise Exception(prefs.EXCEPTION_MSG_DURATION_ERROR)
            
        duration = fileobject.read(8)
        duration = struct.unpack('>d', duration)

        return duration[0]


def WriteMkvDuration(filename:str, duration:float):
    with open(filename, "r+b") as fileobject:
        fileobject.seek(0x160, os.SEEK_SET)
        tag = fileobject.read(3)
        tag = struct.unpack('BBB', tag)

        # Check if the file is a RECOVERED video SEGMENT.
        # It will have a tag   0xEC, 0x01, 0x00   followed by   0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00
        if tag == (0xEC, 0x01, 0x00):
            tag = fileobject.read(8)
            tag = struct.unpack('BBBBBBBB', tag)
            if tag == (0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00):
                #Write a new tag
                fileobject.seek(0x160, os.SEEK_SET)
                fileobject.write(b'\x44\x89\x88')
                tag = (0x44, 0x89, 0x88) #Set correct value to not generate exception below

        if tag != (0x44, 0x89, 0x88):
            raise Exception(prefs.EXCEPTION_MSG_DURATION_ERROR)

        duration = struct.pack('>d', duration)
        fileobject.write(duration)
    





def is_Segment_Size_Valid(filename:str) -> bool:
    with open(filename, "rb") as fileobject:
        #Navigate to segment element
        fileobject.seek(0x2F, os.SEEK_SET)
        tag = fileobject.read(5)
        tag = struct.unpack('BBBBB', tag)
        if tag == (0x18, 0x53, 0x80, 0x67, 0x01):
            tag = fileobject.read(7)
            tag = struct.unpack('BBBBBBB', tag)
            if tag == (0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF):
                print('Debug - Found a file with unknown segment size.')
                return False
            else:
                return True
        else:
            print(f'DEBUG - The file does not have segment size in the correct place. Is this a videofile? : {filename}')
            return False
                    
        
def fix_Segment_Size(filename:str) -> bool:
    with open(filename, "r+b") as fileobject:
        #Get file size
        fileobject.seek(0x00, os.SEEK_END) # 0 bytes from the end of file
        file_size = fileobject.tell()      # Report position
        
        #Navigate to segment element
        fileobject.seek(0x2F, os.SEEK_SET) #For these particular MKV video files this is at offset 0x2F
        tag = fileobject.read(5)
        tag = struct.unpack('BBBBB', tag)
        if tag == (0x18, 0x53, 0x80, 0x67, 0x01):
            #Go to correct location
            fileobject.seek(0x33, os.SEEK_SET)
            
            #The most significant byte is reserved for encoding the length of the size field
            size = file_size - 59
            size =      size & 0x00FFFFFFFFFFFFFF #Clear the most significant byte
            size =      size | 0x0100000000000000 #Set the most significant byte to 0x01

            #Convert size to 8 bytes
            size = struct.pack('>Q', size)
            
            #Write the correct segment size
            fileobject.write(size)
        else:
            print(f'DEBUG - This file is not a correctly formatted mkv videofile. No segment size correction was done to {filename}')







def fixMkv(allMedia:list[MediaClip]):
    DescriptionPrinted = False

    videoFiles = list(filter(lambda x: (x.trackType == prefs.TrackType.VIDEO), allMedia)) #Extract only the videofiles
    videoFiles = sorted(videoFiles, key = lambda x: (x.trackNumber, x.startTime))         #Sort by trackNumber then startTime


    for clip in tqdm(videoFiles): #tqdm creates a progress bar while iterating through allMedia

        mkvDuration = ReadMkvDuration(clip.mediaFile) 
        endFrame = clip.subClips[-1].endFrame
        tagDuration = float((40 * (endFrame + 1)))

        if  mkvDuration != tagDuration:
            #There is a discrepancy between the duration property in the file and the .tag file.
            #The .mkv file will be patched.                

            if mkvDuration == -1.0:
                print("DEBUG - Found a recovered file")
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
        
        #Fix segment size if it is unknown.
        if not is_Segment_Size_Valid(clip.mediaFile):
            fix_Segment_Size(clip.mediaFile)

    print()
    print()









if __name__ == "__main__":
    allMedia = GetAllMedia()
    fixMkv(allMedia)
    