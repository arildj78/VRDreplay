import prefs

class Timeline:
    name : str
    startTime : float
    endTime : float
    
    def __init__(self, timeline) -> None:
        self.timeline = timeline

    def __str__(self) -> str:
        return f'{self.name}\t{self.startTime}\t{self.endTime}'

    def coversTimestamp(self, timeToCheck : float) -> bool:
        if (timeToCheck >= self.startTime) and (timeToCheck <= self.endTime):
            result = True
        else:
            result = False
        
        return result
    
    def TimestampToFrameID(self, timestamp:float) -> float:
        floatFrameID = (timestamp - self.startTime) * prefs.TIMELINE_FPS
        frameID = round(floatFrameID, 0)

        return frameID
            

