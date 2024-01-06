import prefs
from datetime import datetime
from mediaClip import MediaClip
from tqdm import tqdm


GOOD_FILE_TIME = 1577833200    #2020-01-01
good_file_time_string = datetime.fromtimestamp(GOOD_FILE_TIME).strftime("%d %b %Y") #dd mmm yyyy


class Frame:
    frameSecond: str            # e.g.  0.080000     (This is the third frame with 40ms per frame)
    frameTimeString : str       # e.g.  1230768129   (Jan 01 2009 00:02:09)
    frameNanoSecString: str     # e.g.  72884553     (0.072884553 sec)
    NumberOfDatalines : int
    data : list[str]
    timeSinceLastFrame : float

    @property
    def frameTime(self) -> float:
        #Convert Time of frame from string to an float.
        unixTime = float(self.frameTimeString)
        nanoSec = float(self.frameNanoSecString) / 1e9

        return unixTime + nanoSec


    # a setter function
    @frameTime.setter
    def frameTime(self, a):
        fTime = int(a)
        self.frameTimeString = str(fTime)
        self.frameNanoSecString = str(int(1e9 * (a - fTime)))



    def __init__(self) -> None:
        self.data = []



def PrintDescription(filenames: list[str]):
    print("********************************************")
    print("    FIX OF .TAG START TIME                  ")
    print("********************************************")
    print("    If the recording starts before the      ")
    print("    system has updated it's internal clock, ")
    print("    the tag file will show that the clip    ")
    print("    starts at 1 JAN 2009 and suddenly       ")
    print("    jumps to correct time, mid clip.        ")
    print("                                            ")
    print("    This script patches the .tag file       ")
    print("    by back calculating the start time      ")
    print("    from the frame with the first correct   ")
    print("    time. Correct time is defiend as any    ")
    print("    date greater than or equal to           ")
    print("    " + good_file_time_string                )
    print("                                            ")
    print("********************************************")
    print("The file(s) changed by this patch:          ")
    for filename in filenames:
        print(filename                                  )
    print("********************************************")

    
def readTagfile(filename:str, mediaType:prefs.TrackType) -> list[Frame]:
    frames: list[frame]
    frames = []
    
    with open(filename) as tagFile:
        while True:
            try:
                frame = Frame()
                
                frame.frameSecond        = next(tagFile)
                frame.frameTimeString    = next(tagFile)
                frame.frameNanoSecString = next(tagFile)
                                
                if mediaType == prefs.TrackType.VIDEO:
                    frame.NumberOfDatalines = int(next(tagFile))
                    for i in range(frame.NumberOfDatalines):
                        dataLine = next(tagFile)
                        frame.data.append(dataLine)

                frames.append(frame)

            except StopIteration:
                break
            except Exception as e:
                print(f"This didn't go as well. File:{filename} Error:{str(e)}")
    return frames


def writeTagFile(filename:str, frames:list[Frame], mediaType:prefs.TrackType):
    with open(filename, 'wb') as tagFile:
        for frame in frames:
            tagFile.write(lineToByteArray(frame.frameSecond))
            tagFile.write(lineToByteArray(frame.frameTimeString))
            tagFile.write(lineToByteArray(frame.frameNanoSecString))

            if mediaType == prefs.TrackType.VIDEO:
                tagFile.write(lineToByteArray(str(frame.NumberOfDatalines)))
                for dataLine in frame.data:
                    tagFile.write(lineToByteArray(dataLine))



def ApplyPatch(frames: list[Frame]) -> list[Frame]:
    lastFrameTime = 0
    foundGoodTimestamp = False

    #Read forward to find a good datetime
    for i in range(len(frames)):
        thisFrameTime = frames[i].frameTime

        if thisFrameTime >= GOOD_FILE_TIME: #DateTime is >= e.g. 2020-01-01 00:00:00 set in constant at the top
            foundGoodTimestamp = True
            goodFrameNumber = i
            frames[i].timeSinceLastFrame = 0.040   #40ms per frame is assumed since framerate is aprx 25fps
            lastFrameTime = thisFrameTime
            break
        else:
            frames[i].timeSinceLastFrame = thisFrameTime - lastFrameTime
            lastFrameTime = thisFrameTime

    #Calculate backwards from the good datetime
    if foundGoodTimestamp:
        for i in range(goodFrameNumber, 0, -1):
            frames[i-1].frameTime = lastFrameTime - frames[i].timeSinceLastFrame
            lastFrameTime = frames[i-1].frameTime

    return frames
    

def PrintAllStartTimes(allMedia:list[MediaClip]):
    DescriptionPrinted = False

    videoFiles = list(filter(lambda x: (x.trackType == prefs.TrackType.VIDEO), allMedia)) #Extract only the videofiles
    videoFiles = sorted(videoFiles, key = lambda x: (x.trackNumber, x.startTime))

    audioFiles = list(filter(lambda x: (x.trackType == prefs.TrackType.AUDIO), allMedia)) #Extract only the videofiles
    audioFiles = sorted(audioFiles, key = lambda x: (x.trackNumber, x.startTime))

    print("VideoFiles")
    print("*********************************************************")
    for clip in videoFiles:
        print(f'{clip.startTimeString}\t{clip.mediaFile}')

    print()
    print("AudioFiles")
    print("*********************************************************")
    for clip in audioFiles:
        print(f'{clip.startTimeString}\t{clip.mediaFile}')




def fixTagWrongStartTime(allMedia:list[MediaClip]):
    fixedFiles = []

    for clip in tqdm(allMedia):  #tqdm creates a progress bar while iterating through allMedia 
        frames = readTagfile(clip.tagFile, clip.trackType)

        if NeedsPathcing(frames):
            printDescription = True          # Description of patch needs to be printed in the console
            fixedFiles.append(clip.tagFile)  # Append filename so it can be included when printing description
            frames = ApplyPatch(frames)
            writeTagFile(clip.tagFile, frames, clip.trackType)

    if len(fixedFiles) > 0:
        PrintDescription(fixedFiles)         # Print description of patch with the name of fixed files




# Helper function to create an array of characters
# ending with a single 0x0a as the newline character
# Any CR or LF in the input is stripped away.
#***************************************************  
def lineToByteArray(line: str) -> any:
    #Strip away all CR or LF at the end of line
    while True:
        lastByte = ord(line[-1])
        
        if lastByte == 0x0a or lastByte == 0x0d:
            if len(line) > 1:
                line = line[:-1]
            else:
                line = chr(0x0a)  #Entire input was CR or LF.
                break
        else:
                line = line + chr(0x0a)
                break
            
    #String to array of bytes
    result = bytes(line, "UTF-8")
    return result


def NeedsPathcing(frames : list[Frame]) -> bool:
    if frames[0].frameTime < GOOD_FILE_TIME:
        return True
    else:
        return False










if __name__ == "__main__":
    #fixTagWrongStartTime(r"C:\vrd\FeilStartTid\EO_ACT_0000_028\EO_ACT_0000_028.tag", prefs.TrackType.VIDEO)
    
    from getAllMedia import GetAllMedia

    allMedia = GetAllMedia([r'C:\vrd\2023-03-07 MPDLS i skred',])

    fixTagWrongStartTime(allMedia)

