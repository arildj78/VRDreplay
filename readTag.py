import datetime
import prefs

class Frame:
    frameTime: float
    frameNumber = int
    frameMM : int
    frameSS : int
    frameFF : int
    unixTime: int
    nanosec: int
    nanoTime: int
    ms_since_last_frame: float
    correctionFrames: int #0=No correction. 1=Correct for a short frame(~0 ms)   -1=Correct for a long frame (80 ms)
    data: list[int]

    def __init__(self) -> None:
        self.data = []
        self.ms_since_last_frame = -1
        self.correctionFrames = 0


    def __str__(self) -> str:
        result = (str(self.frameNumber) + '\t' +
                  "%d:%02d:%02d" % (self.frameMM, self.frameSS, self.frameFF) + '\t' +
                  "%d" % self.nanoTime + '\t' +
                  "%.2f" % self.ms_since_last_frame)
        return result
    
    def __lt__(self, other):
        return self.frameNumber < other.frameNumber
    
 
class SubClip:
    framerate: float
    startFrame : int
    endFrame : int
    recordFrameFirst : int
    clipFirstFrame : int
    startUnixTime : int
    startNanoSec : int
    
    @property
    def StartSec(self) -> float:
        return self.startUnixTime + self.startNanoSec/1e9
    
    @property
    def EndSec(self) -> float:
        return self.StartSec + self.frameCount / self.framerate

    @property
    def frameCount(self) -> int:
        return self.endFrame - self.startFrame
    
    @property
    def frameCount(self) -> int:
        return self.endFrame - self.startFrame + 1
    
    @property
    def recordFrameLast(self) -> int:
        return self.recordFrameFirst + self.frameCount - 1
    
    def __init__(self, clipFirstFrame, startFrame, endFrame, recordFrameFirst, startUnixTime, startNanoSec) -> None:
        self.framerate = prefs.TIMELINE_FPS
        self.clipFirstFrame = clipFirstFrame
        self.startFrame = startFrame
        self.endFrame = endFrame
        self.recordFrameFirst = recordFrameFirst
        self.startUnixTime = startUnixTime
        self.startNanoSec = startNanoSec

    def __str__(self) -> str:
        result = ("%d" % self.startFrame + '\t' +
                  "%d" % self.endFrame + '\t' +
                  "%d" % self.recordFrame )
        return result




import time
#Instrumentation of code
# t0 = time.perf_counter_ns()
# t1 = time.perf_counter_ns()
# print(f'It took {(t1-t0)/1e6} ms to process the tag-file.')



def ReadTag(tagFile:str, trackType:prefs.TrackType) -> list[SubClip]:
    frames: list[Frame] = []
    #Read the tag-file into the list of frames
    with open(tagFile, 'r') as fileobject:
        while True:
            try:
                str_frameTime = next(fileobject)
                str_unixtime  = next(fileobject)
                str_nanosec   = next(fileobject)
                
                #Only video .tag files have additional datalines
                if trackType == prefs.TrackType.VIDEO:
                    str_dataLines = next(fileobject)
                else:
                    str_dataLines = "0"


                frame = Frame()

                #Convert Time of frame from string to an integer. Rounding is due to floating point accuracy issues
                frame.frameTime = float( str_frameTime )
                frame.frameNumber = int(round( frame.frameTime * prefs.TIMELINE_FPS, 0 ))

                #Convert frame number to minutes:seconds:frames
                ss, ff = divmod(frame.frameNumber, prefs.TIMELINE_FPS)   #TODO REMOVE THIS COMMENT +1 one because next frame is the one that needs to be removed.
                mm, ss = divmod(ss, 60)

                frame.frameMM = mm
                frame.frameSS = ss
                frame.frameFF = ff


                frame.unixTime = int( str_unixtime )
                frame.nanosec  = int( str_nanosec )

                frame.nanoTime = frame.unixTime * 1e9 + frame.nanosec

                #Read through the lines with additional data 
                NumberOfDataLines = int(str_dataLines)
                for dLine in range(NumberOfDataLines):
                    str_DataLine = next(fileobject)
                    #frame.data.append( str_DataLine )   #For now, discard the datalines.

                frames.append(frame)
            except StopIteration:
                break
            except Exception as e:
                print(f"This didn't go as well. File:{tagFile} Error:{str(e)}")



    #Calculate frame durations
    frames[0].ms_since_last_frame = float('inf') #Set first frame to infinite duration

    for i in range(1,len(frames)):
        frameTimeThis = frames[i-1].nanoTime
        frameTimeNext = frames[i].nanoTime
        
        ms = (frameTimeNext - frameTimeThis) / 1e6
        frames[i].ms_since_last_frame = round(ms, 2)
    

    #Extract the frames with duration below 20ms
    missingFrames = [x for x in frames if x.ms_since_last_frame < 20]
    longFrames = [x for x in frames if x.ms_since_last_frame > 60]
    longFrames.pop(0) #Remove first entry. This is a frame that has infinate duration because there was no frame in front

    #Number to be used below when calculating previousEndFrame 
    for frame in missingFrames:
        frame.correctionFrames = 1

    #Number to be used below when calculating previousEndFrame 
    for frame in longFrames:
        frame.correctionFrames = -1


    if len(longFrames) > 50:
        print(tagFile, "has many long frames: ", len(longFrames))

    #weirdFrames = missingFrames + longFrames 
    weirdFrames = missingFrames #TODO - add longframes back in. It has been removed to speed up import until a more efficient solution is developed.


    weirdFrames.sort()
    

    subClip : SubClip
    subClips : list[SubClip]
    subClips = []
    
    clipStartUnixTime = datetime.datetime.utcfromtimestamp(frames[0].unixTime).time()
    clipStartSecInteger = (clipStartUnixTime.hour * 3600 +
                           clipStartUnixTime.minute * 60 +
                           clipStartUnixTime.second)
    clipStartSec = clipStartSecInteger + frames[0].nanosec / 1e9
    clipFirstFrame = int(round(clipStartSec * 25, 0))

    previousEndFrame = -1
    recordFrameFirst = 0


    for frame in weirdFrames:
        subClip = SubClip(clipFirstFrame = clipFirstFrame,  
                          startFrame = previousEndFrame + 1,  #Startframe is inclusive)
                          endFrame = frame.frameNumber - 1,
                          recordFrameFirst = recordFrameFirst,
                          startUnixTime = frame.unixTime,
                          startNanoSec = frame.nanosec)  

        recordFrameFirst = recordFrameFirst + subClip.frameCount
        previousEndFrame = subClip.endFrame + frame.correctionFrames  #The +1 will skip the bad frame
        
        subClips.append(subClip)

    # Add a subclip at the end (if no missing frames this will be the only one added)
    frame = frames[-1]
    subClip = SubClip(clipFirstFrame, 
                      previousEndFrame + 1,  #Startframe is inclusive)
                      frame.frameNumber,
                      recordFrameFirst,
                      startUnixTime = frame.unixTime,
                      startNanoSec = frame.nanosec)                        
    
    subClips.append(subClip)
    
    return subClips



if __name__ == "__main__":
    tagfilename = r"F:\AW101\\tempCopy\\MCC_0000_000\\MCC_0000_000.tag"

    subClips = ReadTag(tagfilename)