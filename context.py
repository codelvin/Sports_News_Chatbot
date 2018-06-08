import sportReference as sr
import Queue
import nltk
import csv
import parsingTools as pt 
import copy
import re

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

	def __repr__(self): #might have to re-add sportRefs as parameter
		#self.sportRefs = sportRefs
		return "Date: %s\nStat: %s\nPlayer: %s\nTeam1: %s\nTeam2: %s\nLocation1: %s\nLocation2: %s\n\n" %(self.date, self.stat, self.player, self.team1, self.team2, self.location1, self.location2)

#-----------------------------------------------------------------------------------------------


def getDate():
	return  str(pt.dateMentioned(tokens))

def getSeason():
	return str(pt.seasonMentioned(tokens))

def getStats():
	return str(pt.statsMentioned(example, basketballRef))

def getPlayer():
	return str(pt.playerMentioned(tagged, basketballRef))

#this one is special - there are two teams
def getTeam1():
	return str(pt.teamsMentioned(tagged, basketballRef)[0])

def getTeam2():
	return str(pt.teamsMentioned(tagged, basketballRef)[1])

def getLocation1():
	return str(pt.locationMentioned(tokens, basketballRef)[0])

def getLocation2():
	return str(pt.locationMentioned(tokens, basketballRef)[1])


#------------------------------------------------------------------------------------------------

rosters = ['rosters/baseball_rosters', 'rosters/basketball_rosters', 'rosters/football_rosters']
roster_dicts = []
stats = ['stats/baseballPlayerStats.txt', 'stats/basketballPlayerStats.txt', 'stats/footballPlayerStats.txt']
stat_lists = []

def fill_rosters():
	i = 0
	for sport in rosters:
		reader = csv.reader(open(sport, 'r'))
		roster_dicts.append({})
		for row in reader:
			roster_dicts[i][row[0]] = row[1:]
		i += 1

def fill_stats():
	for sport in stats:
		reader = open(sport)
		stat_lists.append(reader.read().splitlines())

fill_rosters()
fill_stats()
baseballRef = sr.sportReference("baseball", "teamDictionaries/Baseball Dictionary.xlsx", stat_lists[0], roster_dicts[0])
basketballRef = sr.sportReference('basketball', 'teamDictionaries/Basketball Dictionary.xlsx', stat_lists[1], roster_dicts[1])
footballRef = sr.sportReference('football', 'teamDictionaries/Football Dictionary.xlsx', stat_lists[2], roster_dicts[2])

#-----------------------------------------------------------------------------------------------

class ContextTracker:

	frameTracker = Queue.LifoQueue()

	def __init__(self, sportRefs): #might have to re-add sportRefs as parameter
		self.sportRefs = sportRefs
		self.currFrame = None

	def __repr__(self, tracker): #might have to re-add sportRefs as parameter
					#self.sportRefs = sportRefs
		return "First Frame: %s\n Second Frame: %s\n\n" %(self.frameTracker, self.frameTracker)


		#if we add sports, add locations. right now we dont use location ( we just end up with teams)
	def new_frame(self, sport = None, team1 = None, team2 = None, location1 = None, location2 = None, stat = None, player = None, date = None):
		newFrame = ContextFrame()

		#first create context from only the question itself
		
		if getDate() != "None":
			newFrame.date=getDate()
		elif getSeason() != "None":
			newFrame.date = getSeason()

		if getStats() != "None":
			newFrame.stat = getStats()

		if getPlayer() != "None":
			newFrame.player = getPlayer()
			newFrame.team1 = basketballRef.get_player_team(newFrame.player)

		if getTeam1() != "None":
			newFrame.team1 = getTeam1()

		if getTeam2() !="None":
			newFrame.team2 = getTeam2()

		if getLocation1() != "None":
			if newFrame.team1 !=None:
				newFrame.team2 = getLocation1()
			else:
				newFrame.team1 = getLocation1()
		if getLocation2() != "None":
			newFrame.team2 = getLocation2()


		# Assign values to all of newFrame's member variables here
		# self.currFrame refers to the most recent frame we've seen

		self.currFrame = newFrame
		self.pushFrame()
		#print(self.currFrame)

	def printTracker(self):
		print(self.frameTracker.qsize())
		while not self.frameTracker.empty():
			print(self.frameTracker.get())


	def pushFrame(self):
		if self.frameTracker.qsize() == 6:
			self.frameTracker.get()

		self.frameTracker.put(self.currFrame)



	def categorize(current):
		#if there is a Player
		if current.player != "None":
			if current.stat != None: #there is a stats
				if current.date == None:
					print('There is no date. General Player Stats Question')
				else:
					print('There is a date. Player Game/Season Stat Question')
			else: #there is no stats - so performance
				if current.date != None:
					print('There is no stat. There is a date. Player Game/Season Performance Question')
				else:
					print('There is no stat and there is no date. Player Performance Question')

		else: #there is no player
			if current.team1 != "None": 
				if current.stat != None: #there is a stat
					if current.date != None:
						print('Team Game Stats Question')
					else:
						print('Team General Stats Question')
				else: #there is no stats - so performance
					if current.date != None:
						print('There is no stat. There is a date. Team Game/Season Performance Question')
					else:
						print('There is no stat. There is no date. Team Performance Question')
		
	def addContext(self):

		copyTracker = Queue.LifoQueue()
		copyTracker.queue = copy.deepcopy(self.frameTracker.queue)
		baseArray = list(copyTracker.queue)
		contextArray = list(reversed(baseArray))
		#print contextArray[0]
		#print contextArray[1]
		current = contextArray[0]
		precessor = contextArray[1]
		#print(copyTracker.qsize())

		if current.player != "None" and current.date == None and current.stat == None: #Only Player name given (whenever player is given we have team)
			if precessor.date != None: #take date of game from old context
				current.date = precessor.date
			if precessor.stat != None:
				current.stat = precessor.stat
			else:
				return '3', current

		if current.team1 != "None" and current.player == "None" and current.date == None and current.stat == None: #only team name given
			if precessor.date != None:
				current.date = precessor.date
			if precessor.stat != None:
				current.stat = precessor.stat
			else:
				return '7', current


		if current.stat != None and current.team1 == "None" and current.player == "None" and current.date == None: #only stat word given
			if precessor.player != "None":
				current.player = precessor.player
				if precessor.date != None:
					current.date = precessor.date
			elif precessor.team1 != "None":
				current.team1 = precessor.team1
				if precessor.date != None:
					current.date = precessor.date
			else:
				print('Please provide more information about the team/player you are asking about.')


		if current.date != None and current.team1 == "None" and current.player == "None" and current.stat == None:
			if precessor.player != "None":
				current.player = precessor.player
				if precessor.stat != None:
					current.stat = precessor.stat
			elif precessor.team1 != "None":
				current.team1 = precessor.team1
				if precessor.stat != None:
					current.stat = precessor.stat
			else:
				print('Please provide more information about what event you are referring to on this date.')

#--------------------------------------------CATEGORIZING------------------------------------------------
#[1] Player General Stats
#[2] Player Game Stats
#[3] Player General Performance
#[4] Player Game Performance
#[5] Team General Stats
#[6] Team Game Stats
#[7] Team General Performance
#[8] Team Game Performance

		if current.player != "None":
			if current.stat != None: #there is a stats
				if current.date == None:
					return '1', current
				else:
					return '2', current
			else: #there is no stats - so performance
				if current.date != None:
					return '4', current
				else:
					return '3', current

		else: #there is no player
			if current.team1 != "None": 
				if current.stat != None: #there is a stat
					if current.date != None:
						return '6', current
					else:
						return '5', current
				else: #there is no stats - so performance
					if current.date != None:
						return '8', current
					else:
						return '7', current		 

#------------------------------------------------------------------------------------------------------------
ourContextTracker = ContextTracker(basketballRef)

#examples = ['How did Anthony Brown play?']
examples = ['How many points did Anthony Brown score on 3-28-18?',
			'How many did Stephen Curry?']
			#'How many minutes did Ian Clark play against the Kings?',
			#'Did Los Angeles play the Bulls on Monday?',
			#Did the Warriors play the Nets on Friday?']

for example in examples:
	print(example)
	tokens = nltk.word_tokenize(example)
	tagged = nltk.pos_tag(tokens)
	ourContextTracker.new_frame()



#ourContextTracker.printTracker()
hey = ourContextTracker.addContext()
print hey


#testing for one example at a time

"""example1 ="Lonzo Ball played on Wednesday night against the Celtics."
print(example1)
tokens = nltk.word_tokenize(example1)
tagged = nltk.pos_tag(tokens)
ourContextTracker.new_frame()"""
"""
print("DATE MENTIONED: " + str(pt.dateMentioned(tokens)))
print("SEASON MENTIONED: " + str(pt.seasonMentioned(tokens)))
print("STATS MENTIONED: " + str(pt.statsMentioned(example1, basketballRef)))
print("PLAYER MENTIONED: " + str(pt.playerMentioned(tagged, basketballRef)))
print("TEAM MENTIONED: " + str(pt.teamsMentioned(tagged, basketballRef)))
print("LOCATION MENTIONED: " + str(pt.locationMentioned(tokens, basketballRef)))"""