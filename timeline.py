class Timeline:
    name : str
    startTime : float
    endTime : float
    
    def __init__(self, timeline) -> None:
        self.timeline = timeline

    def coversTimestamp(self, timeToCheck : float) -> bool:
        if (timeToCheck >= self.startTime) and (timeToCheck <= self.endTime):
            result = True
        else:
            result = False
        
        return result
            

