import dateutil.parser as dparser
import datetime
import enchant

seasonWords = ["season", "spring", "summer", "fall", "winter", "year"]
injuryWords = ["injury", "injured", "hurt", "out", "broken", "broke"]
gamePerformance = ["play", "do", "peform"]
weekdayWords = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"]
dayPhrases = {"last night": -1, "this morning": 0, "this afternoon": 0, "yesterday": -1, "today": 0, "tonight": 0}

# THE FOLLOWING FUNCTIONS ARE HELPERS THAT YOU SHOULDN'T NEED
#
#
#
# checks for 4 digit numbers in text
def checkforYear(string):
    if len(string) != 4:
        return False

    for c in string:
        if c.isalpha():
            return False

    return True

def checkforDate(tokens):
    sentence = ' '.join(tokens)
    try:
        date = dparser.parse(sentence, fuzzy=True, dayfirst=False)
        for word in tokens:
            if word.lower() in weekdayWords:
                date = date - datetime.timedelta(days=7)

        return date.date().strftime("%m-%d-%y")
    except ValueError:
        for phrase in dayPhrases.keys():
            if phrase in sentence:
                date = datetime.datetime.now() + datetime.timedelta(days=dayPhrases[phrase])
                return date.strftime("%m-%d-%y")

        return None

def checkYearOnly(tokens):
    new_tokens=[]
    for word in tokens:
        if not checkforYear(word):
           new_tokens.append(word)

    if checkforDate(new_tokens) == None:
        return True

    return False

def nouns(tagged):
    nouns = []
    for word in tagged:
        if word[1].startswith('NN'):
            nouns.append(word[0])
    return nouns

def nouns_pairs(tagged):
    pairs = []
    for first, second in zip(tagged, tagged[1:]):
        if first[1].startswith('NN') | second[1].startswith('NN'):
            pairs.append((first[0],second[0]))
    return pairs

dictionary = enchant.Dict("en_US")

# END HELPER FUNCTIONS #
#
#


# THIS IS THE START OF THE FUNCTIONS YOU WILL NEED #
#
#
#

# must use dateMentioned first, otherwise you could find a season when there is actually a date
# returns year of the season being discussed, or None
def seasonMentioned(tokens):
    for word in tokens:
        if word in seasonWords:
            return datetime.datetime.now().year
        if checkforYear(word):
            return word

    return None

def dateMentioned(tokens):
    date = checkforDate(tokens)
    if date != None and not checkYearOnly(tokens):
        return date

    return None

def statsMentioned(question, sportRef):
    for stat in sportRef.stats:
        if stat.lower() in question.lower():
            return stat
    return None


def playerMentioned(tagged_question, sportRef):
    pairs = nouns_pairs(tagged_question)
    for pair in pairs:
        player_name = pair[0] + " " + pair[1]
        if (sportRef.playerExists(player_name)):
            return player_name

    return None

def teamsMentioned(tagged_question, sportRef):
    nounlist = nouns(tagged_question)
    teams = []
    for word in nounlist:
        found = sportRef.teamExists(word)
        if found != None and found not in teams:
            teams.append(found)

    pairs = nouns_pairs(tagged_question)
    for pair in pairs:
        team_name = pair[0] + " " + pair[1]
        found = sportRef.teamExists(team_name)
        if found != None and found not in teams:
            teams.append(found)

    if len(teams) > 0:
        return teams

    return None


def locationMentioned(tokenized_question, sportRef):
    for word in tokenized_question:
        if not dictionary.check(word.lower()) or word == 'Buffalo' or word == 'Phoenix':
            if sportRef.locationHasTeam(word.lower()):
                return word.lower()

    for first, second in zip(tokenized_question, tokenized_question[1:]):
        if not dictionary.check(first.lower()) and not dictionary.check(second.lower()):
            location = first.lower() + " " + second.lower()
            if sportRef.locationHasTeam(location):
                return location

    return None
