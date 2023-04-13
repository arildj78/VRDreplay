import datetime

#F:\AW101\Disk1\vrd_database
#tagfilename = "G:/VRD Dump/2023-03-07 MPDLS i skred/vrd_database/EO_ACT/EO_ACT_0000/EO_ACT_0000_014/EO_ACT_0000_014.tag"
tagfilename =                        "F:/AW101/Disk1/vrd_database/EO_ACT/EO_ACT_0000/EO_ACT_0000_013/EO_ACT_0000_013.tag"
#tagfilename = "G:/VRD Dump/2023-03-07 MPDLS i skred/vrd_database/EO_OPP/EO_OPP_0000/EO_OPP_0000_022/EO_OPP_0000_022.tag"

class Frame:
    frameTime: float
    frameNumber = int
    frameMM : int
    frameSS : int
    frameFF : int
    unixTime: int
    nanosec: int
    nanoTime: float
    duration: float
    data: list[int]

    def __init__(self) -> None:
        self.data = []



frames: list[Frame] = []

import time
#Instrumentation of code
# t0 = time.perf_counter_ns()
# t1 = time.perf_counter_ns()
# print(f'It took {(t1-t0)/1e6} ms to process the tag-file.')




#Read the tag-file into the list of frames
with open(tagfilename, 'r') as fileobject:
    while True:
        try:
            str_frameTime = next(fileobject)
            str_unixtime  = next(fileobject)
            str_nanosec   = next(fileobject)
            str_dataLines = next(fileobject)

            frame = Frame()

            #Convert Time of frame from string to an integer. Rounding is due to floating point accuracy issues
            frame.frameTime = float( str_frameTime )
            frame.frameNumber = int(round( frame.frameTime * 25, 0 ))

            #Convert frame number to minutes:seconds:frames
            ss, ff = divmod(frame.frameNumber+1, 25)   #+1 one because next frame is the one that needs to be removed.
            mm, ss = divmod(ss, 60)

            frame.frameMM = mm
            frame.frameSS = ss
            frame.frameFF = ff


            unixtime = int( str_unixtime )
            nanosec  = int( str_nanosec )

            frame.nanoTime = unixtime * 1e9 + nanosec

            #Read through the lines with additional data 
            NumberOfDataLines = int(str_dataLines)
            for dLine in range(NumberOfDataLines):
                str_DataLine = next(fileobject)
                #frame.data.append( str_DataLine )   #For now, discard the datalines.

            #frames.append(frame)
        except StopIteration:
            break
        except:
            print("Something else went wrong")


#Calculate frame durations
for i in range(len(frames)-1):
    frameTimeThis = frames[i].nanoTime
    frameTimeNext = frames[i+1].nanoTime
    
    ms = (frameTimeNext - frameTimeThis) / 1e6
    frames[i].duration = round(ms, 2)

frames[len(frames)-1].duration = float('inf')


#Extract the frames with duration below 20ms
abc = [x for x in frames if x.duration < 20]

print()
print()
print('*********************************************')
print('The frames with duration less than 20 ms are:')
print(tagfilename)
print('*********************************************')
print()
print('Frame\tTimeCode\tDuration (ms)')
print('----------------------------------------------')

for f in abc:
    tc = "%d:%02d:%02d" % (f.frameMM, f.frameSS, f.frameFF)
    print(f'{f.frameNumber}\t{tc}\t\t{f.duration}')

clipDuration = (frames[len(frames)-1].nanoTime - frames[0].nanoTime) / 1e9
clipDurationFrames = 25 * clipDuration

ss, ff = divmod(clipDurationFrames, 25)
mm, ss = divmod(clipDuration, 60)
print()
print(f'The clip duration is %01d:%02d:%02d' % (mm, ss, ff))
print(f'The number of frames are:\t{len(frames)}')
print()
print()



startTime1 = frames[0].nanoTime

