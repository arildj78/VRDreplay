import struct, os
from datetime import datetime
import re #regEx library
import daVinciConnection
from findUSBdevice import get_vrdDrives
import prefs

from timeline import Timeline

class Event:
    time : int
    description: str
    path : str

    # The string representation of the instance
    def __str__(self) -> str:
        time = datetime.utcfromtimestamp(self.time)
        return f'{time.strftime("%Y-%m-%d  %H:%M:%S")}\t{self.path}'

    def __lt__(self, other):
        return (self.time, self.path) < (other.time, other.path)




class EvtFile:
    #Record length is 144
    class Record:
        LENGTH = 144
        formatString = '<2q32s12q'  #Little endian, 2 x int64, 32 char string, 12 x int64
        print()

        time, \
        unk1, \
        description, \
        unk2, \
        unk3, \
        unk4, \
        unk5, \
        unk6, \
        unk7, \
        unk8, \
        unk9, \
        unk10, \
        unk11, \
        unk12, \
        unk13 = [0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        manualEvent = False  

        def __init__(self, buffer) -> None:
            self.time, \
            self.unk1, \
            self.description, \
            self.unk2, \
            self.unk3, \
            self.unk4, \
            self.unk5, \
            self.unk6, \
            self.unk7, \
            self.unk8, \
            self.unk9, \
            self.unk10, \
            self.unk11, \
            self.unk12, \
            self.unk13 = struct.unpack(EvtFile.Record.formatString, buffer)

            self.description = self.description.split(b'\x00')[0].decode('utf-8')
            if self.unk9 == 0:
                self.manualEvent = True


    def __init__(self, eventFilename:str):
        self.eventFilename = eventFilename 
        self.records:list[EvtFile.Record] = []
        self.ReadFileContent()

    def ReadFileContent(self):
        with open(self.eventFilename, 'rb') as f:
            while True:
                buf = f.read(EvtFile.Record.LENGTH)
                if buf == b'':
                    break
                newRecord = EvtFile.Record( buf ) 
                self.records.append(newRecord)
    
    def Length(self) -> int:
        return len(self.records)
    



    



def GetUniqueEvents(directories = None) -> list[Event]:
    if directories == None:
        directories = get_vrdDrives()


    #Initialize an empty list to hold a reference to the media files beeing imported
    events: list[Event] = []

    #Create regex objects to identify the files to import
    regex_event = re.compile(prefs.EVT_FILENAME_REGEX)

    #Look through all directories and subdirectories for all files and process them
    for dir in directories:
        for root, dirs, files in os.walk(dir):
            for file in files:

                #Check if file is an Event file
                if regex_event.match(file):
                    filename = os.path.join(root, file)
                    evtFile = EvtFile(filename)
                    for evt in evtFile.records:
                        #Only process the manual events. Start and Stop events are ignored.
                        if evt.manualEvent: 
                            event = Event()
                            event.path = filename
                            event.description = evt.description
                            event.time = evt.time
                            events.append(event)
    
    events.sort()

    uniqueEvents:list[event]
    uniqueEvents = []

    if len(events) > 0:
        uniqueEvents.append(events[0])

    for event in events:
        if event.time != uniqueEvents[-1].time:
            uniqueEvents.append(event)
    
    return uniqueEvents


def CreateEventMarkerClip(project):
    """_summary_

    Args:
        project (DaVinci Resolve Project): Generated by ProjectManager.CreateProject()
        framesDuration (int): Duration of the marker clip

    Returns:
        MediaPoolItem: Returns the media pool item corresponding to the newly created event marker clip.
    """
    
    
    import DaVinciResolveScript as dvrs

    # major objects
    resolve = dvrs.scriptapp("Resolve")

    mediaPool = project.GetMediaPool()
    timeLine = mediaPool.CreateEmptyTimeline("temporary")
    
    fusionTimeLine = timeLine.InsertFusionCompositionIntoTimeline()
    
    fc = fusionTimeLine.GetFusionCompByIndex(1)
    


    # Read the fusion composition that creates the Event Marker Graphics from the file 'event.comp'
    # This file can be modified by creating a new composition and then copying it by selecting all the nodes, Ctrl-C and
    # then pasting it into the file before saving it.
    #with open("C:\\Users\\arild\\AppData\\Roaming\\Blackmagic Design\\DaVinci Resolve\\Support\\Fusion\\Scripts\\Comp\\VRDreplay\\event.comp") as file:
    with open(os.path.dirname(__file__) + "\\fusionComposition\\event.comp") as file:
        data = file.read()

    #Put the composition on the clipboard
    import pyperclip
    pyperclip.copy(data)

    # # Clean the Fusion composition before pasting
    # resolve.OpenPage("fusion")   #Change to Fusion so we can paste the Event Marker Generator
    # listOfTools = fc.GetToolList()
    # listOfTools[1].Delete() #Delete the first tool (should be the only one): Media Out 1











    # Connect Media Out from the import to the existing Media Out
    resolve.OpenPage("fusion")   #Change to Fusion so we can paste the Event Marker Generator
    
    # Paste the composition from the clipboard into Fusion
    
    listOfTools =fc.GetToolList()
    listOfTools[1].Delete() #Delete the first tool (should be the only one): Media Out 1

    fc.Paste()

    # listOfTools =fc.GetToolList()
    #listOfTools[1].Delete() #Delete the first tool (should be the only one): Media Out 1

    # fc.GetToolList()
    # for key in listOfTools:
    #     print(key, '->', listOfTools[key])

    try:
        oldMediaOut = fc.FindTool('MediaOut1')
        oldMediaOut.Delete()
    except:
        raise Exception("Unable to find MediaOut1 after creating a new fusion composition. Call for help :)")

    try:
        LastNode = fc.FindTool('Merge99')
        fc.SetActiveTool(LastNode)
    except:
        print('Unable to find Merge99 which should be the last merge node in the event composition.')


    fc.AddTool('MediaOut', -32768, -32768)
    
    resolve.OpenPage("edit")





    compoundClip = timeLine.CreateCompoundClip(fusionTimeLine)
    mediaPoolItem = compoundClip.GetMediaPoolItem()
    mediaPoolItem.SetClipProperty("Clip Name", "EventGraphic")
    mediaPool.DeleteTimelines(timeLine)

    return mediaPoolItem


def InsertEventMarkerClip(timeLine:Timeline, eventMarkerClip, trackNumber:int, eventTime:int, framesDuration:int):
    recordFrame = timeLine.TimestampToRecordFrame(eventTime)
    
    newClip = {
        "mediaPoolItem" : eventMarkerClip,   #The media file to be inserted
        "trackIndex" : trackNumber,          #Track to insert the media in                e.g. 5
        "startFrame" : 0,                    #The first frame in the media to be used     e.g. 6002
        "endFrame" : framesDuration,         #The last frame in the media to be used      e.g. 7501
        "recordFrame" : recordFrame,         #The timeline location (in frames) to insert the clip at   e.g. 1 239 324 + 6000
    }

    a = timeLine.mediaPool.AppendToTimeline( [newClip] )
    #b = timeLine.timeline.CreateFusionClip(a)






if __name__ == "__main__":
    resolve, projectManager, currentProject, mediaStorage, fusion = daVinciConnection.initConnection()
    CreateEventMarkerClip(currentProject)
 



