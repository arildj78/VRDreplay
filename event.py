import struct, os
from datetime import datetime
import re #regEx library
import daVinciConnection

import prefs

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
    



    



def GetUniqueEvents(directories=prefs.RECORDING_DIRECTORIES) -> list[Event]:
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



if __name__ == "__main__":
    resolve, projectManager, currentProject, mediaStorage, fusion = daVinciConnection.initConnection()
    CreateEventMarkerClip(currentProject)
 



