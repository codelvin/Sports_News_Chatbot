import sportReference as sr
import queue

class ContextFrame:

    def __init__(self):
        self.sport = None
        self.team1 = None
        self.team2 = None
        self.location1 = None
        self.location2 = None
        self.stat = None
        self.player = None
        self.date = None


class ContextTracker:

    frameTracker = queue.LifoQueue()

    def __init__(self, sportRefs):
        self.sportRefs = sportRefs
        self.currFrame = None


    def new_frame(self, sport = None, team1 = None, team2 = None, location1 = None, location2 = None, stat = None, player = None, date = None):
        newFrame = ContextFrame()

        # Assign values to all of newFrame's member variables here
        # self.currFrame refers to the most recent frame we've seen

        self.currFrame = newFrame
        self.pushFrame()


    def pushFrame(self):
        if self.frameTracker.qsize() == 6:
            self.frameTracker.get()

        self.frameTracker.put(self.currFrame)

