import nltk
import csv
import sportReference as sr
import parsingTools as pt
import context as ct 

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


"""examples = ['Lonzo Ball played on Wednesday night against the Celtics.',
            'How many points did Anthony Brown score on 3-28-18?',
            'How many minutes did Ian Clark play against the Kings?',
            'Did Los Angeles play the Bulls on Monday?',
            'Did the Warriors play the Nets on Friday?']"""

ourContextTracker = ct.ContextTracker()

"""for ex in examples:
    print(ex)
    tokens = nltk.word_tokenize(ex)
    tagged = nltk.pos_tag(tokens)
    ourContextTracker.new_frame()
    print("DATE MENTIONED: " + str(pt.dateMentioned(tokens)))
    print("SEASON MENTIONED: " + str(pt.seasonMentioned(tokens)))
    print("STATS MENTIONED: " + str(pt.statsMentioned(ex, basketballRef)))
    print("PLAYER MENTIONED: " + str(pt.playerMentioned(tagged, basketballRef)))
    print("TEAM MENTIONED: " + str(pt.teamsMentioned(tagged, basketballRef)))
    print("LOCATION MENTIONED: " + str(pt.locationMentioned(tokens, basketballRef)))
    print()"""

example1 ="Lonzo Ball played on Wednesday night against the Celtics"

print(example1)
tokens = nltk.word_tokenize(example1)
tagged = nltk.pos_tag(tokens)
ourContextTracker.new_frame()

#we need these because tokens that will be the parameter are located here, not in pt

def getDate():
	return  str(pt.dateMentioned(tokens))

def getSeason():
	return str(pt.seasonMentioned(tokens))

def getStats():
	return str(pt.statsMentioned(ex, basketballRef))

def getPlayer():
	return str(pt.playerMentioned(tagged, basketballRef))

#this one is special - there are two teams
def getTeams():
	return str(pt.teamsMentioned(tagged, basketballRef))

def getLocation():
	return str(pt.locationMentioned(tokens, basketballRef))

