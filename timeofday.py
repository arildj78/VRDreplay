import struct, os
from datetime import datetime
import re #regEx library
import daVinciConnection

import prefs

from timeline import Timeline

class TimeOfDay:
    time : int
    description: str
    path : str

    # The string representation of the instance
    def __str__(self) -> str:
        time = datetime.utcfromtimestamp(self.time)
        return f'{time.strftime("%Y-%m-%d  %H:%M:%S")}\t{self.path}'

    def __lt__(self, other):
        return (self.time, self.path) < (other.time, other.path)




def CreateTimeOfDayClip(project):
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
    
    fusionTimeLineItem = timeLine.InsertFusionCompositionIntoTimeline()
    
    
    fc = fusionTimeLineItem.GetFusionCompByIndex(1)
    


    # Read the fusion composition that creates the Time Of Day Graphics from the file 'timeofday.comp'
    # This file can be modified by creating a new composition and then copying it by selecting all the nodes, Ctrl-C and
    # then pasting it into the file before saving it.
    with open(os.path.dirname(__file__) + "\\fusionComposition\\timeofday.comp") as file:
        data = file.read()

    #Put the composition on the clipboard
    import pyperclip
    pyperclip.copy(data)



    # Connect Media Out from the import to the existing Media Out
    resolve.OpenPage("fusion")   #Change to Fusion so we can paste the Time Of Day generator
    
    # # Clean the Fusion composition before pasting
    listOfTools =fc.GetToolList()
    listOfTools[1].Delete() #Delete the first tool (should be the only one): Media Out 1
   
   # Paste the composition from the clipboard into Fusion
    fc.Paste()

    try:
        LastNode = fc.FindTool('Time99')
        LastNode.SetInput("Input_hh",23)
        LastNode.SetInput("Input_mm",58)
        LastNode.SetInput("Input_ss",59)
        LastNode.SetInput("Input_ff",24)
        fc.SetActiveTool(LastNode)
    except:
        print('Unable to find Time99 which should be the last node (and only node) in the event composition.')


    fc.AddTool('MediaOut', -32768, -32768)
    
    resolve.OpenPage("edit")





    compoundClip = timeLine.CreateCompoundClip(fusionTimeLineItem)
    mediaPoolItem = compoundClip.GetMediaPoolItem()
    mediaPoolItem.SetClipProperty("Clip Name", "Time of Day")
    mediaPool.DeleteTimelines(timeLine)

    return mediaPoolItem







if __name__ == "__main__":
    resolve, projectManager, currentProject, mediaStorage, fusion = daVinciConnection.initConnection()
    CreateTimeOfDayClip(currentProject)
 



