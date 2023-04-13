import os

#Class to hold information on a single clip beeing imported
class MediaClip:
    mediaFile : str
    tagFile : str
    trackType : str
    trackNumber : int
    trackName : str
    startTime : int
    stopTime : int
    startOfTimeline : bool
    timelineNumber : int

    @property
    def duration_sec(self):
        result = self.stopTime - self.startTime
        return result


    def __init__(self) -> None:
        self.startOfTimeline = False
        self.timelineNumber = 0
        pass

    #String representation of the mediaclip. Useful during development and debugging
    def __str__(self) -> str:
        result = str(self.timelineNumber) + '\t'
        result = result + str(self.startOfTimeline) + '\t'
        result = result + os.path.basename(self.mediaFile).ljust(26) + '\t'
        result = result + os.path.basename(self.tagFile).ljust(26) + '\t'
        result = result + self.trackType + '\t'
        result = result + str(self.trackNumber) + '\t'
        result = result + self.trackName.ljust(11) + '\t'
        result = result + str(self.startTime) + '\t'
        result = result + str(self.stopTime) + '\t'
        result = result + str(self.duration_sec)

        return result

    #Methods to be used when comparing clips. Necessary for sorting algorithm
    def __lt__(self, obj):
        return (self.startTime, self.trackNumber) < (obj.startTime, obj.trackNumber)
  
    def __gt__(self, obj):
        return (self.startTime, self.trackNumber) > (obj.startTime, obj.trackNumber)

    def __le__(self, obj):
        return (self.startTime, self.trackNumber) <= (obj.startTime, obj.trackNumber)

    def __ge__(self, obj):
        return (self.startTime, self.trackNumber) >= (obj.startTime, obj.trackNumber)

    def __eq__(self, obj):
        return (self.startTime, self.trackNumber) == (obj.startTime, obj.trackNumber)

