import sportReference as sr
import Queue
import driver 
import parsingTools as pt 

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

    frameTracker = Queue.LifoQueue()

    def __init__(self): #might have to re-add sportRefs as parameter
        #self.sportRefs = sportRefs
        self.currFrame = None

        #if we add sports, add locations
    def new_frame(self, sport = None, team1 = None, team2 = None, location1 = None, location2 = None, stat = None, player = None, date = None):
        newFrame = ContextFrame()

        #first check driver to see if we can grab context from question.

        
        if driver.getDate() != None:
            newFrame.date=driver.getDate()
        elif driver.getSeason() != None:
            newFrame.date = driver.getSeason()
        #else look in past frames


        if driver.getStats() != None:
            newFrame.stat = driver.getStats()
        #else look in past frames


        if driver.getPlayer() != None:
            newFrame.player = driver.getPlayer()
        #find team of player, set team as well
        #else look in past frames


        if driver.getTeam() != None:
            newFrame.team1 = driver.getTeams()[0]
            if driver.getTeams()[1] !=None:
                newFrame.team2 = driver.getTeams()[1]
        #else look at players, fill in from roster (player team = team1)
        #else look at past contexts






        # Assign values to all of newFrame's member variables here
        # self.currFrame refers to the most recent frame we've seen

        self.currFrame = newFrame
        self.pushFrame()
        print("Help")
        print(currFrame)

    #def addContext():
        #if we cant answer the question, look in past context frames


    def pushFrame(self):
        if self.frameTracker.qsize() == 6:
            self.frameTracker.get()

        self.frameTracker.put(self.currFrame)


